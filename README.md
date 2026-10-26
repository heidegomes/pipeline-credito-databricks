# pipeline-credito-databricks

# Pipeline Lakehouse para Análise de Risco de Crédito e Perfil de Associados 🟢

Este projeto apresenta o desenvolvimento de um pipeline de dados robusto, utilizando a **Arquitetura Medallion (Bronze, Silver e Gold)** dentro da plataforma **Databricks**. O objetivo principal é processar dados de propostas de crédito e movimentações financeiras para calcular indicadores críticos de risco (como taxas de inadimplência) e traçar o perfil socioeconômico dos associados, simulando um cenário real de inteligência de dados para o **Sicredi**.

O projeto foi construído pensando na eficiência de custos em nuvem, governança de dados e na geração de insights rápidos para apoiar a tomada de decisão das cooperativas e agências regionais.

---

## 📐 Arquitetura do Pipeline de Dados

O pipeline foi estruturado de forma linear e incremental utilizando **Delta Lake**, garantindo transações ACID e alta performance de leitura e escrita.

```
[Dados Brutos / CSV] ──► [Bronze: Ingestão/Metadados] ──► [Silver: Limpeza/LGPD] ──► [Gold: KPIs/Z-ORDER] ──► [Machine Learning: MLflow]
```

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

*   **Databricks (Community Edition):** Ambiente de desenvolvimento unificado e gerenciamento de clusters Spark.
*   **Apache Spark (PySpark & Spark SQL):** Motor de processamento distribuído para tratamento de Big Data.
*   **Delta Lake:** Armazenamento em formato open-source (transações ACID).
*   **Scikit-Learn & MLflow:** Algoritmo preditivo (Random Forest) e governança/versionamento de modelos de IA.

---

## 📂 Detalhamento das Camadas do Projeto

### 1. Camada Bronze (01_camada_bronze.ipynb)
*   **Abordagem:** Ingestão otimizada via Spark utilizando inferência de esquema automático (`inferSchema`). Adição da coluna `data_ingestao` com carimbo de data/hora para garantir a linhagem e auditabilidade do dado (Data Lineage).

### 2. Camada Silver (02_camada_silver.ipynb)
*   **Abordagem:** Tratamento de *outliers* de cadastro e preenchimento de valores nulos com lógica condicional (`when`/`otherwise`). Adequação das colunas de inglês para a taxonomia oficial do cooperativismo de crédito do Sicredi (Termos como *Associado*, *Valor Solicitado* e *Score de Crédito*).

### 3. Camada Gold (03_camada_gold.ipynb)
*   **Abordagem:** Cálculo de KPIs de negócio como o volume total solicitado, médias de renda e a taxa de inadimplência real (*Default Rate*) agrupada por score de crédito. Aplicação de `OPTIMIZE` e `Z-ORDER BY` para reorganizar os arquivos fisicamente em disco e acelerar futuras consultas de BI.

### 4. Camada de Machine Learning (04_machine_learning_risco.ipynb)
*   **Abordagem:** Treinamento de um modelo de classificação utilizando **Random Forest** para prever o risco de inadimplência de novos associados baseado em seu perfil socioeconômico. Integração com o **MLflow** para registro automático de métricas de acurácia.

---
## 🚀 Como Executar este Projeto
1. Crie uma conta gratuita no Databricks Community Edition e ative um cluster Single Node.
2. Faça o upload do arquivo de dados para o DBFS.
3. Importe os quatro notebooks deste repositório para o seu Workspace.
4. Execute os notebooks em sequência para processar os dados e treinar o modelo de IA.
