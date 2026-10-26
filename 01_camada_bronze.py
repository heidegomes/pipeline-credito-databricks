# Databricks notebook source
# 1. Ler os dados diretamente do Unity Catalog usando o caminho completo
df_bruto = spark.table("workspace.default.credit_risk_dataset_2")

# COMMAND ----------

# 2. Adicionar carimbo de data/hora para auditoria (Data Lineage)
from pyspark.sql.functions import current_timestamp
df_bronze = df_bruto.withColumn("data_ingestao", current_timestamp())

# COMMAND ----------

# 3. Salvar no formato moderno Delta Lake na camada bronze
df_bronze.write.format("delta").mode("overwrite").saveAsTable("workspace.default.bronze_propostas_credito")

# COMMAND ----------

# 4. Visualizar o resultado da tabela criada
display(spark.table("workspace.default.bronze_propostas_credito").limit(5))