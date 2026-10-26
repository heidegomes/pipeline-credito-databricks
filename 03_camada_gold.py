# Databricks notebook source
# MAGIC %sql
# MAGIC -- NOTEBOOK 3: CAMADA GOLD (Linguagem: SQL)
# MAGIC -- Objetivo: Agregações de negócio, cálculo de KPIs financeiros e Tuning de Performance
# MAGIC
# MAGIC CREATE OR REPLACE TABLE workspace.default.gold_analise_risco_score AS
# MAGIC SELECT 
# MAGIC     nota_credito_score AS score_credito,
# MAGIC     COUNT(*) AS total_propostas_avaliadas,
# MAGIC     SUM(valor_solicitado) AS volume_total_solicitado,
# MAGIC     ROUND(AVG(renda_anual), 2) AS media_renda_anual,
# MAGIC     -- Cálculo real do Default Rate (Taxa de Inadimplência)
# MAGIC     ROUND((SUM(CASE WHEN status_inadimplencia = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS taxa_inadimplencia_percentual
# MAGIC FROM workspace.default.silver_propostas_credito
# MAGIC GROUP BY nota_credito_score
# MAGIC ORDER BY nota_credito_score;
# MAGIC
# MAGIC -- Otimização Física de arquivos no disco para acelerar consultas e relatórios
# MAGIC OPTIMIZE workspace.default.gold_analise_risco_score 
# MAGIC ZORDER BY (score_credito);
# MAGIC
# MAGIC -- Visualizar o resultado final da Camada Gold
# MAGIC SELECT * FROM workspace.default.gold_analise_risco_score;