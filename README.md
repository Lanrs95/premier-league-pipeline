Premier League Data Pipeline

Pipeline de dados desenvolvido como case executivo para análise e engenharia de dados utilizando estatísticas históricas e recentes da Premier League.
O objetivo é consolidar dados de múltiplas fontes em um fluxo de ingestão, tratamento, curadoria e orquestração no ambiente Google Cloud Platform (GCP), seguindo boas práticas de arquitetura de dados e governança.

📌 Objetivo do Projeto

Construir um pipeline de dados confiável e escalável que:

Integre diferentes datasets da Premier League (times, jogadores, partidas, eventos).

Padronize e trate dados para análises consistentes.

Implemente segurança e anonimização de dados sensíveis conforme a LGPD.

Disponibilize informações para consumo em BI e Machine Learning.

☁️ Acesso aos Dados no GCP

Os dados utilizados no projeto estão armazenados no bucket:

gs://meu-bucket-premier/bronze/
gs://meu-bucket-premier/silver/
gs://meu-bucket-premier/gold/


Atenção: O acesso é restrito e requer permissões no projeto nice-proposal-467718-q6 no GCP.
Para demonstração pública, disponibilizamos um exemplo de dataset Bronze:
📂 Acessar exemplo Bronze

🗂 Arquitetura do Pipeline

Etapas:

Bronze – Ingestão dos dados brutos no Cloud Storage.

Silver – Padronização de tipos, tratamento de nulos, remoção de duplicatas e aplicação de regras de negócio.

Gold – Modelagem de tabelas de fato e dimensões para análise.

Consumo – Disponibilização para BI, dashboards e modelos de Machine Learning.

🔑 Pré-requisitos

Conta no Google Cloud Platform (GCP) com permissões para:

Criar e acessar Cloud Storage Buckets

Criar e executar notebooks no Vertex AI Workbench

Python 3.10+ (no ambiente do GCP)

Bibliotecas Python:

pandas
pyarrow
google-cloud-storage
pyspark

▶️ Como Executar

Acesse o Vertex AI Workbench no seu projeto GCP.

Clone este repositório no ambiente do notebook:

git clone https://github.com/seu_usuario/seu_repo.git


Ajuste as variáveis no início de cada notebook (BUCKET_NAME, PROJECT_ID, etc.).

Execute os notebooks na ordem:

01_bronze_ingestao.ipynb – Ingestão e salvamento particionado.

02_silver_tratamentos.ipynb – Limpeza, padronização e aplicação de regras.

03_gold_marts.ipynb – Criação de tabelas de consumo.

04_quality_checks.ipynb – Validações de qualidade (Great Expectations).

05_scheduler_pipeline.ipynb – Orquestração e logs.

📊 Resultados Esperados

Tabelas Gold prontas para análise.

Métricas-chave: gols, xG, posse de bola, finalizações, assistências.

Relatórios e dashboards executivos.

Estrutura escalável e replicável.

📎 Contato

Allan Ribeiro – LinkedIn
📧 Email: allan.silva@santander.com.br
