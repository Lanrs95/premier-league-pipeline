#!/usr/bin/env python3
"""
Orquestrador local de notebooks (Bronze -> Silver -> Gold)
Uso:
  python run_pipeline.py --project nice-proposal-467718-q6 --bucket meu-bucket-premier \
    --region us-west1 --timestamp auto
Requisitos: pip install -r requirements.txt
"""
import argparse, sys, os, subprocess, datetime as dt, io, fnmatch
from pathlib import Path
import nbformat as nbf

DEFAULT_ORDER = [
    # TENTA USAR versão limpa, senão cai para original
    "Camada_Bronze_clean.ipynb|Camada_Bronze.ipynb",
    "mascaramento.ipynb",
    "players_silver.ipynb",
    "teams_silver.ipynb",
    "matches_silver.ipynb",
    "players_gold.ipynb",
    "teams_gold.ipynb",
    "matches_gold.ipynb",
]

def ensure_pkgs():
    pkgs = ["papermill", "google-cloud-storage", "pandas", "pyarrow", "gcsfs"]
    for p in pkgs:
        try:
            __import__(p.split("-")[0])
        except Exception:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", p])

def find_nb(name_or_pipe: str) -> str:
    """Accept pattern like 'A|B' and return first that exists."""
    for candidate in name_or_pipe.split("|"):
        if Path(candidate).exists():
            return candidate
    return name_or_pipe  # fallback (will error later if not found)

def inject_parameters(nb_path: Path, params: dict, force_kernel_py3=True) -> Path:
    nb = nbf.read(nb_path.as_posix(), as_version=4)
    # parameters cell
    lines = [f"{k} = {repr(v)}" for k, v in params.items()]
    src = "# parameters (injetado pelo orquestrador)\n" + "\n".join(lines) + "\n"
    cell = nbf.v4.new_code_cell(src)
    cell.metadata = {"tags": ["parameters"]}
    nb.cells.insert(0, cell)
    # kernel
    if force_kernel_py3:
        nb.metadata["kernelspec"] = {"display_name":"Python 3","language":"python","name":"python3"}
    # write temp
    tmp = nb_path.with_name(nb_path.stem + ".__tmp__.ipynb")
    nbf.write(nb, tmp.as_posix())
    return tmp

def run_nb(in_nb: str, out_nb: str, params: dict):
    import papermill as pm
    pm.execute_notebook(input_path=in_nb, output_path=out_nb, kernel_name="python3",
                        parameters=params, report_mode=False, progress_bar=False)

def main():
    ensure_pkgs()
    import papermill as pm
    from google.cloud import storage

    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--bucket", required=True)
    ap.add_argument("--region", default="us-west1")
    ap.add_argument("--timestamp", default="auto", help='"auto" ou valor fixo (YYYYmmdd-HHMMSS)')
    ap.add_argument("--dryrun", action="store_true", help="Só mostra ordem e sai")
    args = ap.parse_args()

    run_ts = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S") if args.timestamp=="auto" else args.timestamp
    print("RUN_TS:", run_ts)

    # monta parâmetros comuns
    params = {
        "PROJECT_ID": args.project,
        "REGION": args.region,
        "BRONZE_PATH": f"gs://{args.bucket}/bronze/",
        "SILVER_PATH": f"gs://{args.bucket}/silver/",
        "GOLD_PATH":   f"gs://{args.bucket}/gold/",
        "RUN_TS": run_ts,
    }

    # resolve ordem efetiva
    order = [find_nb(x) for x in DEFAULT_ORDER]
    print("Ordem:", order)
    if args.dryrun:
        return 0

    # estrutura de logs no GCS
    client = storage.Client(project=args.project)
    bucket = client.bucket(args.bucket)
    runs_prefix = f"orchestration/runs/{run_ts}"
    logs_prefix = f"orchestration/logs/{run_ts}"

    def gcs_upload_text(rel_path: str, text: str, content_type="text/plain"):
        blob = bucket.blob(rel_path)
        blob.upload_from_string(text, content_type=content_type)

    # executa
    for nb in order:
        if not Path(nb).exists():
            print(f"[ERRO] Notebook não encontrado: {nb}")
            return 2
        step = Path(nb).stem
        print(f"\n=== [{step}] ===")
        try:
            # injeta parameters e força kernel
            tmp_nb = inject_parameters(Path(nb), params, force_kernel_py3=True)
            out_nb = f"_out_{step}_{run_ts}.ipynb"
            run_nb(tmp_nb.as_posix(), out_nb, params)
            # sobe output como log rico
            with open(out_nb, "rb") as f:
                bucket.blob(f"{logs_prefix}/{out_nb}").upload_from_string(f.read(), content_type="application/x-ipynb+json")
            gcs_upload_text(f"{runs_prefix}/{step}_SUCCESS.json", '{"ok": true}')
            print(f"[{step}] OK")
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            gcs_upload_text(f"{runs_prefix}/{step}_FAILED.json", tb)
            print(f"[{step}] FALHOU ->", e)
            return 3

    print("\n✅ Pipeline executado com sucesso (modo local).")
    print("Marcas:", f"gs://{args.bucket}/{runs_prefix}")
    print("Logs:  ", f"gs://{args.bucket}/{logs_prefix}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
