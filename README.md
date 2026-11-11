# Pipeline Lakehouse para Análise de Risco de Crédito e Perfil de Associados 🟢

Este projeto apresenta o desenvolvimento de um pipeline de dados robusto, utilizando a **Arquitetura Medallion (Bronze, Silver e Gold)** dentro da plataforma **Databricks**. O objetivo principal é processar dados de propostas de crédito e movimentações financeiras para calcular indicadores críticos de risco (como taxas de inadimplência) e traçar o perfil socioeconômico dos associados, simulando um cenário real de inteligência de dados para o **Sicredi**.

O projeto foi construído pensando na eficiência de custos em nuvem, governança de dados e na geração de insights rápidos para apoiar a tomada de decisão das cooperativas e agências regionais.

Como extensão, o pipeline prepara perfis com **identificadores sintéticos** para integração com um **agente de análise de crédito com LangGraph**, conectando a engenharia de dados a uma aplicação com explicação por IA.

*Projeto educacional de portfólio, sem vínculo institucional com o Sicredi.*

---

## 📐 Arquitetura do Pipeline de Dados

O pipeline utiliza **Delta Lake** para armazenar as camadas de dados com suporte a transações ACID. A preparação dos perfis de demonstração parte da camada Silver e permite consultas pelo agente através de um SQL Warehouse.

```text
[Dados Brutos / CSV] ──► [Bronze: Ingestão/Metadados] ──► [Silver: Limpeza/Padronização] ──► [Gold: KPIs/Z-ORDER] ──► [Machine Learning: MLflow]
                                                                  │
                                                                  └──► [Perfis com IDs sintéticos] ──► [SQL Warehouse] ──► [Agente: LangGraph]
```

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Databricks (Free Edition):** Ambiente de desenvolvimento com recursos serverless para notebooks e SQL Warehouse.
* **Apache Spark (PySpark & Spark SQL):** Motor de processamento distribuído para tratamento de Big Data.
* **Delta Lake:** Armazenamento em formato open-source com suporte a transações ACID.
* **Scikit-Learn & MLflow:** Algoritmo preditivo (Random Forest) e registro de métricas e modelos de IA.
* **Databricks SQL Connector & OAuth:** Consulta aos perfis pelo projeto do agente, com autenticação pelo navegador.
* **LangGraph & LangChain:** Orquestração do fluxo e das ferramentas no projeto integrado do agente de crédito.

---

## 📂 Detalhamento das Camadas do Projeto

### 1. Camada Bronze (01_camada_bronze.py)

* **Abordagem:** Ingestão otimizada via Spark utilizando inferência de esquema automático (`inferSchema`). Adição da coluna `data_ingestao` com carimbo de data/hora para garantir a linhagem e auditabilidade do dado (Data Lineage).

### 2. Camada Silver (02_camada_silver.py)

* **Abordagem:** Tratamento de *outliers* de cadastro e preenchimento de valores nulos com lógica condicional (`when`/`otherwise`). Adequação das colunas de inglês para a taxonomia do cenário de cooperativismo de crédito (termos como *Associado*, *Valor Solicitado* e *Score de Crédito*).

### 3. Camada Gold (03_camada_gold.py)

* **Abordagem:** Cálculo de KPIs de negócio como o volume total solicitado, médias de renda e a taxa de inadimplência (*Default Rate*) agrupada por score de crédito. Uso de `OPTIMIZE` e `Z-ORDER BY` no notebook para reorganizar os arquivos fisicamente em disco e apoiar consultas de BI, conforme a compatibilidade dos recursos no ambiente utilizado.

### 4. Camada de Machine Learning (04_machine_learning_risco.py)

* **Abordagem:** Treinamento de um modelo de classificação utilizando **Random Forest** para prever o risco de inadimplência de novos associados baseado em seu perfil socioeconômico. Integração com o **MLflow** para registro automático de métricas de acurácia.

### 5. Perfis de Demonstração (05_preparar_perfis_demo.ipynb)

* **Abordagem:** Criação da tabela `workspace.default.silver_perfis_credito_demo` a partir da Silver, mantendo os atributos do perfil e adicionando `id_proposta_demo`, `cpf` e `identificador_sintetico`. A tabela original é preservada.
* **Identificadores fictícios:** Os CPFs possuem 11 dígitos e verificador deliberadamente inválido. São utilizados apenas como chaves de consulta no projeto, sem representar documentos válidos.
* **Integração:** Os perfis são consultados pelo agente de crédito através do SQL Warehouse, permitindo avaliar a nota de crédito, o histórico de inadimplência e o comprometimento da renda mensal informada.

Como o dataset original não possui uma chave de pessoa, cada linha recebe uma identidade fictícia independente. O ID identifica a proposta na cópia; não permite reconhecer um mesmo associado em propostas diferentes. A geração desses identificadores não anonimiza os demais atributos da base.

---

## 🤖 Integração com o Agente de Crédito

Este pipeline está conectado ao projeto [Agente de Análise de Crédito com LangGraph](https://github.com/heidegomes/agente-analise-credito).

O agente consulta a tabela preparada no notebook 5, calcula o percentual de comprometimento da renda e aplica uma política ilustrativa em Python: nota A ou B, ausência de histórico de inadimplência e parcela de até 30% da renda mensal. Opcionalmente, um modelo de linguagem explica o parecer.

**Exemplo:** para uma renda mensal de R$ 5.000 e parcela de R$ 800, o comprometimento é de 16%, dentro do limite. Ainda assim, o pedido pode ser recusado se a nota do perfil estiver fora das faixas A e B.

A integração atual utiliza os atributos da Silver; as previsões do modelo Random Forest ainda não são consumidas pelo agente. As regras de decisão são educacionais e não representam uma política validada para concessão real de crédito.

---

## 🚀 Como Executar este Projeto

1. Acesse seu workspace no **Databricks Free Edition** e utilize o compute serverless disponível.
2. Disponibilize os arquivos de dados e ajuste os caminhos de leitura, catálogo e schema utilizados pelos notebooks ao seu ambiente.
3. Importe os **cinco notebooks** deste repositório para uma pasta do Workspace. Os arquivos `.py` usam o formato source do Databricks, e o notebook 5 utiliza `.ipynb`.
4. Execute Bronze e Silver antes das etapas que consomem suas tabelas. Em seguida, execute Gold e Machine Learning conforme as entradas definidas nos notebooks.
5. Execute o notebook 5 após a Silver para criar a tabela de perfis com identificadores sintéticos. Reutilize a tabela criada para manter a associação entre os perfis e seus identificadores nos testes.
6. Para testar o agente, inicie o SQL Warehouse e siga as instruções do [repositório do agente](https://github.com/heidegomes/agente-analise-credito), configurando `DATABRICKS_AUTH_TYPE=oauth` e `DATABRICKS_TABLE=workspace.default.silver_perfis_credito_demo` no `.env` local.

*Os caminhos e recursos de versões anteriores do Databricks, como DBFS e clusters Single Node, precisam ser adaptados quando o notebook for executado na Free Edition.*
