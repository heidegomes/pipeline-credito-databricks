# Databricks notebook source
# COMMAND ----------
# NOTEBOOK 4: MACHINE LEARNING (Nome: 04_machine_learning_risco | Linguagem: Python)
# Objetivo: Demonstrar ciclo básico de ML (Treino, Teste) e uso do MLflow (MLOps)

from pyspark.sql.functions import col
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import mlflow

# COMMAND ----------
# 1. Carregando dados limpos da Silver (com o catálogo workspace correto) e convertendo para Pandas
df_spark = spark.table("workspace.default.silver_propostas_credito")
df_ml = df_spark.toPandas()

# COMMAND ----------
# 2. Definindo variáveis de entrada (X) e alvo (y)
features = ["idade_associado", "renda_anual", "valor_solicitado", "tempo_trabalho_anos"]
X = df_ml[features]
y = df_ml["status_inadimplencia"]

# COMMAND ----------
# 3. Divisão de dados em Treino (80%) e Teste (20%)
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

# COMMAND ----------
# 4. Registrando o experimento de forma profissional com MLflow (MLOps)
with mlflow.start_run(run_name="Modelo_Risco_Credito_Sicredi"):
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_treino, y_treino) # Treinamento
    previsoes = modelo.predict(X_teste) # Teste
    
    acuracia = accuracy_score(y_teste, previsoes)
    print(f"Acurácia do Modelo: {acuracia * 100:.2f}%")
    
    # Salvando os registros de MLOps no Databricks
    mlflow.log_metric("acuracia", acuracia)
    mlflow.sklearn.log_model(modelo, "modelo_random_forest")

print("\nRelatório Técnico de Classificação:")
print(classification_report(y_teste, previsoes))