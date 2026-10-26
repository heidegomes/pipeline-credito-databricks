# Databricks notebook source
# COMMAND ----------
# NOTEBOOK 2: CAMADA SILVER (Nome: 02_camada_silver | Linguagem: Python)
# Objetivo: Limpeza de dados (Data Quality), LGPD e tradução para termos do Sicredi

from pyspark.sql.functions import col, when, current_timestamp

# 1. Ler da tabela Bronze utilizando o catálogo correto
df_bronze = spark.table("workspace.default.bronze_propostas_credito")


# COMMAND ----------

from pyspark.sql.functions import col, when, current_timestamp
# COMMAND ----------
# 2. Tratamento de Outliers (idade menor que 120) e Nulos (tempo de trabalho nulo vira 0)
df_bronze = spark.table("workspace.default.bronze_propostas_credito")
df_limpo = df_bronze.filter(col("person_age") < 120) \
    .withColumn("person_emp_length", when(col("person_emp_length").isNull(), 0).otherwise(col("person_emp_length")))

# COMMAND ----------

# COMMAND ----------
# 3. Tradução e adequação LGPD (selecionando apenas o necessário para o negócio)
df_silver = df_limpo.select(
    col("person_age").alias("idade_associado"),
    col("person_income").alias("renda_anual"),
    col("person_home_ownership").alias("tipo_moradia"),
    col("person_emp_length").alias("tempo_trabalho_anos"),
    col("loan_intent").alias("objetivo_emprestimo"),
    col("loan_grade").alias("nota_credito_score"),
    col("loan_amnt").alias("valor_solicitado"),
    col("loan_int_rate").alias("taxa_juros_percentual"),
    col("loan_status").alias("status_inadimplencia"), # 0 = Em dia, 1 = Inadimplente
    col("loan_percent_income").alias("percentual_comprometimento_renda"),
    col("cb_person_default_on_file").alias("historico_inadimplencia_previo"),
    col("cb_person_cred_hist_length").alias("tempo_historico_credito_anos")
)

df_silver = df_silver.withColumn("data_atualizacao_silver", current_timestamp())

# COMMAND ----------

# COMMAND ----------
# 4. Salvando a tabela Silver higienizada no catálogo workspace
df_silver.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.silver_propostas_credito")

# COMMAND ----------

# 5. Visualizar o resultado
display(spark.table("workspace.default.silver_propostas_credito").limit(5))