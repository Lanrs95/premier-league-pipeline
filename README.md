# Premier League Data Pipeline

Pipeline de dados desenvolvido como case executivo para análise e engenharia de dados usando dados da Premier League.  
O projeto contempla ingestão, tratamento, curadoria e orquestração em ambiente **Google Cloud Platform (GCP)**.

---

## 📌 Objetivo
Consolidar múltiplos datasets da Premier League (times, jogadores, partidas, eventos) em um fluxo único e padronizado, garantindo qualidade, segurança (LGPD) e disponibilidade para consumo em BI ou modelos de Machine Learning.

---

## 🗂 Arquitetura do Pipeline
![Arquitetura do Pipeline](docs/arquitetura_pipeline.png)

**Etapas:**
1. **Bronze** – Ingestão dos dados brutos no Cloud Storage.
2. **Silver** – Padronização de tipos, tratamento de nulos, remoção de duplicatas e aplicação de regras de negócio.
3. **Gold** – Criação de tabelas de fato e dimensões para análise.
4. **Consumo** – Disponibilização para BI, relatórios executivos e análises avançadas.

---

## 🔑 Pré-requisitos

- Conta no **Google Cloud Platform (GCP)** com permissões para:
  - Criar e acessar **Cloud Storage Buckets**
  - Criar e executar notebooks no **Vertex AI Workbench**
- Dataset carregado nos buckets conforme a estrutura:
  ```
  gs://nome-bucket/bronze/
  gs://nome-bucket/silver/
  gs://nome-bucket/gold/
  ```
- Python 3.10+ (no ambiente do GCP)
- Bibliotecas Python:
  ```
  pandas
  pyarrow
  google-cloud-storage
  pyspark
  ```

---

## ▶️ Como Executar

1. **Acesse o Vertex AI Workbench** no seu projeto GCP.
2. **Clone este repositório** no ambiente do notebook:
   ```bash
   git clone https://github.com/seu_usuario/seu_repo.git
   ```
3. **Ajuste as variáveis** no início de cada notebook (`BUCKET_NAME`, `PROJECT_ID`, etc.).
4. **Execute os notebooks** na ordem:
   1. `01_bronze_ingestao.ipynb` – Leitura bruta + salvamento particionado
   2. `02_silver_tratamentos.ipynb` – Tipos, nulos, duplicatas, regras de negócio
   3. `03_gold_marts.ipynb` – Agregações, dimensões e fatos
   4. `04_quality_checks.ipynb` – Validações de qualidade (Great Expectations)
   5. `05_scheduler_pipeline.ipynb` – Agendamento / Jobs / Logs

---

## 📊 Resultados

- **Tabelas Gold**: fatos e dimensões prontas para consumo.
- **Métricas-chave**: gols, xG, posse de bola, finalizações, assistências.
- **Painel/Relatório**: pronto para visualização executiva.

---

## 📎 Contato

Allan – [LinkedIn](https://www.linkedin.com/](https://www.linkedin.com/in/allan-ribeiro-312029209/)  
📧 Email: contato.allan95@gmail.com
