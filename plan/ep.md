 Plan to implement                                                                                                                                        │
│                                                                                                                                                          │
│ Plano de Execução — Flight Delay Prediction                                                                                                              │
│                                                                                                                                                          │
│ Context                                                                                                                                                  │
│                                                                                                                                                          │
│ Projeto acadêmico (POS Fase 3). O EDA original (eda_flights.ipynb) será reorganizado em 3 notebooks separados: exploração dos dados brutos,              │
│ limpeza/preparação, e análise dos dados limpos. Depois: modelagem supervisionada, não supervisionada e apresentação.                                     │
│                                                                                                                                                          │
│ Status por Requisito do Tech Challenge                                                                                                                   │
│                                                                                                                                                          │
│ ┌──────────────────────────────────────────┬──────────────┬───────────────────────────────────────────────────────┐                                      │
│ │                Requisito                 │    Status    │                        Origem                         │                                      │
│ ├──────────────────────────────────────────┼──────────────┼───────────────────────────────────────────────────────┤                                      │
│ │ EDA: estatísticas descritivas            │ ✅ Concluído │ código existe em eda_flights.ipynb, será reorganizado │                                      │
│ ├──────────────────────────────────────────┼──────────────┼───────────────────────────────────────────────────────┤                                      │
│ │ EDA: visualizações com insights          │ ✅ Concluído │ idem                                                  │                                      │
│ ├──────────────────────────────────────────┼──────────────┼───────────────────────────────────────────────────────┤                                      │
│ │ EDA: tratamento de valores ausentes      │ ✅ Concluído │ idem                                                  │                                      │
│ ├──────────────────────────────────────────┼──────────────┼───────────────────────────────────────────────────────┤                                      │
│ │ Modelagem supervisionada (2+ algoritmos) │ ❌ Pendente  │ → modelagem_supervisionada.ipynb                      │                                      │
│ ├──────────────────────────────────────────┼──────────────┼───────────────────────────────────────────────────────┤                                      │
│ │ Modelagem não supervisionada             │ ❌ Pendente  │ → modelagem_nao_supervisionada.ipynb                  │                                      │
│ ├──────────────────────────────────────────┼──────────────┼───────────────────────────────────────────────────────┤                                      │
│ │ Apresentação crítica dos resultados      │ ❌ Pendente  │ → apresentacao.ipynb                                  │                                      │
│ └──────────────────────────────────────────┴──────────────┴───────────────────────────────────────────────────────┘                                      │
│                                                                                                                                                          │
│ ---                                                                                                                                                      │
│ Decisões Técnicas                                                                                                                                        │
│                                                                                                                                                          │
│ Limpeza de Dados                                                                                                                                         │
│                                                                                                                                                          │
│ A limpeza será um notebook (limpeza.ipynb), não um módulo, porque:                                                                                       │
│ - Projeto acadêmico: o avaliador precisa ver cada decisão explicada passo a passo                                                                        │
│ - A limpeza roda UMA vez para gerar o Parquet — não precisa ser função reutilizável                                                                      │
│ - O notebook É a documentação do pipeline de limpeza                                                                                                     │
│                                                                                                                                                          │
│ Operações de limpeza (em ordem):                                                                                                                         │
│                                                                                                                                                          │
│ ┌───────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────┐  │
│ │                         Operação                          │                                      Justificativa                                      │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ Left join com airlines e airports                         │ Enriquecer com nomes, cidades, estados, coordenadas                                     │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ drop(columns=["YEAR"])                                    │ Sempre 2015, variância zero                                                             │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ drop(columns=["TAIL_NUMBER", "FLIGHT_NUMBER"])            │ Identificadores de alta cardinalidade (4,897 e 6,952 únicos), sem valor preditivo       │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ query("CANCELLED == 0")                                   │ Voos cancelados ≠ atrasados — categoria diferente. ~3,700 cancelados permaneceriam sem  │  │
│ │                                                           │ este filtro.                                                                            │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ drop(columns=["CANCELLED", "CANCELLATION_REASON"])        │ Após filtrar, são constantes (0 e NaN)                                                  │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ fillna(0) nas 5 colunas de causa de atraso                │ NaN = "sem atraso desta causa", não dado faltante                                       │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ dropna(subset=["DEPARTURE_DELAY"])                        │ ~1.5% sem registro de atraso — não modeláveis                                           │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ fillna("Desconhecido") em colunas de join categóricas     │ ~8.3% aeroportos com código FAA numérico sem match IATA                                 │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ Feature engineering: DEP_HOUR, SEASON, IS_WEEKEND,        │ Variáveis derivadas para modelagem                                                      │  │
│ │ IS_DELAYED                                                │                                                                                         │  │
│ ├───────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤  │
│ │ Export Parquet                                            │ Persistir para notebooks seguintes                                                      │  │
│ └───────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                                                          │
│ Resultado: ~5.7M rows × ~36 cols (sem YEAR, TAIL_NUMBER, FLIGHT_NUMBER, CANCELLED, CANCELLATION_REASON)                                                  │
│                                                                                                                                                          │
│ Bibliotecas                                                                                                                                              │
│                                                                                                                                                          │
│ ┌──────────────┬─────────────┬────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────┐  │
│ │  Biblioteca  │ Adicionar?  │               Tarefa               │                                   Justificativa                                   │  │
│ ├──────────────┼─────────────┼────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────┤  │
│ │ scikit-learn │ Já          │ LR, LinearReg, KMeans, PCA,        │ Framework base                                                                    │  │
│ │              │ instalado   │ métricas                           │                                                                                   │  │
│ ├──────────────┼─────────────┼────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────┤  │
│ │ XGBoost      │ ✅          │ Classificação + Regressão          │ Gradient boosting, estado da arte para tabulares, scale_pos_weight para imbalance │  │
│ │              │ Adicionar   │                                    │                                                                                   │  │
│ ├──────────────┼─────────────┼────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────┤  │
│ │ LightGBM     │ ✅          │ Regressão                          │ 2-3x mais rápido que XGBoost (histogram splitting), mostra conhecimento de 2      │  │
│ │              │ Adicionar   │                                    │ frameworks                                                                        │  │
│ ├──────────────┼─────────────┼────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────┤  │
│ │ pyarrow      │ ✅          │ I/O Parquet                        │ Necessário para export/import dos dados limpos                                    │  │
│ │              │ Adicionar   │                                    │                                                                                   │  │
│ └──────────────┴─────────────┴────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                                                          │
│ Algoritmos por Tarefa                                                                                                                                    │
│                                                                                                                                                          │
│ Classificação (IS_DELAYED):     Logistic Regression (baseline)  vs  XGBoost                                                                              │
│ Regressão (DEPARTURE_DELAY):    Linear Regression (baseline)    vs  LightGBM  vs  XGBoost                                                                │
│ Clustering:                     K-Means (perfis de aeroporto)                                                                                            │
│ Redução dimensionalidade:       PCA (causas de atraso)                                                                                                   │
│                                                                                                                                                          │
│ Por que LR vs XGBoost para classificação:                                                                                                                │
│ - Contraste máximo: linear simples vs ensemble não-linear                                                                                                │
│ - XGBoost mais rápido que RF em 4.5M rows, melhor generalização                                                                                          │
│ - scale_pos_weight=4.6 (ratio 82/18) lida com imbalance nativamente                                                                                      │
│ - Feature importance gain-based é mais informativa                                                                                                       │
│                                                                                                                                                          │
│ Por que 3 algoritmos na regressão:                                                                                                                       │
│ - Linear Regression: baseline interpretável                                                                                                              │
│ - LightGBM: mais rápido (histogram binning), ideal para 4.5M rows                                                                                        │
│ - XGBoost: comparação direta com LightGBM mostra trade-off velocidade vs acurácia                                                                        │
│ - Ter 3 modelos na regressão compensa ter 2 na classificação — total de 5 modelos no projeto                                                             │
│                                                                                                                                                          │
│ ---                                                                                                                                                      │
│ Arquitetura de Arquivos                                                                                                                                  │
│                                                                                                                                                          │
│ flight-delay--prediction/                                                                                                                                │
│   pyproject.toml                          # MODIFICAR: + pyarrow, xgboost, lightgbm                                                                      │
│   modules/                                                                                                                                               │
│     __init__.py                           # NOVO                                                                                                         │
│     data_loader.py                        # NOVO: load Parquet, build splits                                                                             │
│     evaluation.py                         # NOVO: métricas e plots de avaliação                                                                          │
│   notebooks/                                                                                                                                             │
│     EDA_exploratorio.ipynb                # NOVO: exploração dados brutos (do CSV)                                                                       │
│     limpeza.ipynb                         # NOVO: pipeline de limpeza → export Parquet                                                                   │
│     EDA_clean.ipynb                       # NOVO: análise dados limpos (do Parquet)                                                                      │
│     modelagem_supervisionada.ipynb        # NOVO: classificação + regressão                                                                              │
│     modelagem_nao_supervisionada.ipynb    # NOVO: PCA + K-Means                                                                                          │
│     apresentacao.ipynb                    # NOVO: resumo para vídeo                                                                                      │
│   data/                                                                                                                                                  │
│     flights_clean.parquet                 # GERADO por limpeza.ipynb (~200-300MB)                                                                        │
│   .gitignore                              # MODIFICAR: + *.parquet                                                                                       │
│                                                                                                                                                          │
│ Nota: eda_flights.ipynb e fly.ipynb existentes serão mantidos como referência mas não fazem parte do fluxo final.                                        │
│                                                                                                                                                          │
│ Fluxo de Dados                                                                                                                                           │
│                                                                                                                                                          │
│ EDA_exploratorio.ipynb                                                                                                                                   │
│   └─ Lê CSV bruto + joins → exploração, missing values, distribuições, cancelamentos                                                                     │
│                                                                                                                                                          │
│ limpeza.ipynb                                                                                                                                            │
│   └─ Lê CSV bruto + joins → drops, filtros, fillna, feature eng → data/flights_clean.parquet                                                             │
│                                                                                                                                                          │
│ EDA_clean.ipynb                                                                                                                                          │
│   └─ Lê Parquet → análise detalhada dos dados limpos, correlações, patterns                                                                              │
│                                                                                                                                                          │
│ modelagem_supervisionada.ipynb                                                                                                                           │
│   └─ Lê Parquet via modules/data_loader → treina e avalia 5 modelos                                                                                      │
│                                                                                                                                                          │
│ modelagem_nao_supervisionada.ipynb                                                                                                                       │
│   └─ Lê Parquet via modules/data_loader → PCA + K-Means                                                                                                  │
│                                                                                                                                                          │
│ apresentacao.ipynb                                                                                                                                       │
│   └─ Lê Parquet → gráficos-chave + resumo de todos os resultados                                                                                         │
│                                                                                                                                                          │
│ ---                                                                                                                                                      │
│ Sequência de Implementação                                                                                                                               │
│                                                                                                                                                          │
│ Passo 1: Dependências                                                                                                                                    │
│                                                                                                                                                          │
│ Arquivo: pyproject.toml                                                                                                                                  │
│ - Adicionar em dependencies: "pyarrow>=19.0"                                                                                                             │
│ - Adicionar em [dependency-groups] dev: "xgboost>=2.1", "lightgbm>=4.5"                                                                                  │
│ - Rodar uv sync --group dev                                                                                                                              │
│                                                                                                                                                          │
│ Passo 2: Criar modules/                                                                                                                                  │
│                                                                                                                                                          │
│ modules/__init__.py — vazio                                                                                                                              │
│                                                                                                                                                          │
│ modules/data_loader.py                                                                                                                                   │
│ - load_flights_clean(path="../data/flights_clean.parquet") -> pd.DataFrame — lê Parquet                                                                  │
│ - build_classification_split(df, seed=42, test_size=0.2) — X (20 features: MONTH, DAY_OF_WEEK, DEP_HOUR, SEASON, IS_WEEKEND, DISTANCE + 14 airline       │
│ dummies), y = IS_DELAYED, split via np.random.default_rng(42)                                                                                            │
│ - build_regression_split(df, seed=42, test_size=0.2) — filtra DEPARTURE_DELAY > 0, y = DEPARTURE_DELAY, mesmas features e esquema de split               │
│                                                                                                                                                          │
│ modules/evaluation.py                                                                                                                                    │
│ - print_classification_report(y_true, y_pred, y_prob, model_name) — accuracy, precision, recall, F1, ROC-AUC; retorna dict                               │
│ - plot_confusion_matrix(y_true, y_pred, model_name) — heatmap seaborn                                                                                    │
│ - plot_roc_curves(results: dict) — curvas ROC sobrepostas                                                                                                │
│ - print_regression_report(y_true, y_pred, model_name) — MAE, RMSE, R²                                                                                    │
│ - plot_residuals(y_true, y_pred, model_name) — scatter de resíduos                                                                                       │
│ - plot_feature_importance(model, feature_names, model_name, top_n=15) — bar horizontal, compatível com sklearn/xgboost/lightgbm                          │
│                                                                                                                                                          │
│ Passo 3: notebooks/EDA_exploratorio.ipynb                                                                                                                │
│                                                                                                                                                          │
│ Exploração dos dados brutos — entender o dataset antes de limpar.                                                                                        │
│                                                                                                                                                          │
│ ┌─────┬──────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │  #  │ Tipo │                                                                Conteúdo                                                                 │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 1   │ md   │ Título: "Análise Exploratória dos Dados — Dados Brutos". Contexto: dataset de 5.8M voos, 2015, US DOT.                                  │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2   │ code │ Imports (pandas, numpy, matplotlib, seaborn) + configs                                                                                  │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3   │ code │ Carregar 3 CSVs + joins (flights, airports, airlines). Print shape (5,819,079 × 42).                                                    │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 4   │ md   │ Explicar as 3 fontes e como foram unidas (left joins). Nota sobre ~8.3% NaN nos joins.                                                  │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 5   │ code │ flights.info(memory_usage='deep') — overview das 42 colunas, tipos, memória (~5GB)                                                      │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 6   │ code │ Tabela de missing values: contagem e % por coluna, ordenado                                                                             │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 7   │ md   │ Estratégia de Missing Values: explicar os 3 padrões (causas de atraso ~82% by design, cancelamentos ~98.5%, departure_delay ~1.5%       │ │
│ │     │      │ realmente faltante, joins ~8.3%)                                                                                                        │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 8   │ code │ flights.describe() — estatísticas descritivas de todas as numéricas                                                                     │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 9   │ code │ Histogramas de DEPARTURE_DELAY e ARRIVAL_DELAY (clipped para visualização)                                                              │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 10  │ code │ Taxa de cancelamento + gráfico de razões de cancelamento (A/B/C/D)                                                                      │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 11  │ code │ Avg departure delay por AIRLINE_NAME (bar chart com nomes completos)                                                                    │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 12  │ code │ Avg departure delay por MONTH (sazonalidade)                                                                                            │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 13  │ code │ Avg departure delay por DAY_OF_WEEK                                                                                                     │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 14  │ code │ Avg departure delay por hora do dia (SCHEDULED_DEPARTURE // 100)                                                                        │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 15  │ code │ Top 15 aeroportos por avg delay (com nomes completos)                                                                                   │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 16  │ code │ Top 10 estados por avg delay                                                                                                            │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 17  │ code │ Correlation heatmap (seaborn) das variáveis numéricas de delay                                                                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 18  │ code │ Avg delay minutes por causa (para voos atrasados)                                                                                       │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 19  │ code │ Outliers extremos: contagem de delays > 300 min                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 20  │ md   │ Conclusões da Exploração: padrões identificados, problemas a corrigir, decisões de limpeza necessárias. Apontar para o notebook de      │ │
│ │     │      │ limpeza.                                                                                                                                │ │
│ └─────┴──────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                                                                          │
│ Passo 4: notebooks/limpeza.ipynb                                                                                                                         │
│                                                                                                                                                          │
│ Pipeline de limpeza — transforma dados brutos em dados prontos para modelagem.                                                                           │
│                                                                                                                                                          │
│ ┌─────┬──────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │  #  │ Tipo │                                                                Conteúdo                                                                 │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 1   │ md   │ Título: "Limpeza e Preparação dos Dados". Explicar: este notebook lê os CSVs brutos, aplica todas as transformações e exporta o         │ │
│ │     │      │ resultado em Parquet.                                                                                                                   │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2   │ code │ Imports + carregar 3 CSVs + joins (mesmo código do EDA_exploratorio)                                                                    │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3   │ md   │ Remoção de colunas sem valor preditivo: YEAR (constante), TAIL_NUMBER e FLIGHT_NUMBER (identificadores de alta cardinalidade)           │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 4   │ code │ flights.drop(columns=["YEAR", "TAIL_NUMBER", "FLIGHT_NUMBER"]) + print shape                                                            │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 5   │ md   │ Remoção de voos cancelados: cancelados não são "atrasados", são categoria diferente. Manter confundiria a modelagem.                    │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 6   │ code │ flights.query("CANCELLED == 0").drop(columns=["CANCELLED", "CANCELLATION_REASON"]) + print shape e rows removidos                       │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 7   │ md   │ Tratamento de colunas de causa de atraso: NaN = "sem atraso desta causa". Imputar com 0.                                                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 8   │ code │ fillna(0) nas 5 colunas de causa                                                                                                        │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 9   │ md   │ Remoção de registros sem DEPARTURE_DELAY: ~1.5% sem dado operacional. Não modeláveis.                                                   │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 10  │ code │ dropna(subset=["DEPARTURE_DELAY"]) + print shape e % retido                                                                             │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 11  │ md   │ Tratamento de NaN em colunas de join: aeroportos com código FAA numérico sem match IATA. Preencher com "Desconhecido".                  │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 12  │ code │ fillna("Desconhecido") nas 6 colunas categóricas de join                                                                                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 13  │ md   │ Feature Engineering: criar variáveis derivadas para modelagem.                                                                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 14  │ code │ DEP_HOUR, SEASON, IS_WEEKEND, IS_DELAYED. Print sample e distribuições.                                                                 │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 15  │ md   │ Verificação final: conferir shape, tipos, ausência de nulls em colunas críticas.                                                        │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 16  │ code │ Shape final, missing values check, describe() do dataset limpo                                                                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 17  │ md   │ Exportação em Parquet: salvar para evitar reprocessamento nos notebooks seguintes.                                                      │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 18  │ code │ to_parquet("../data/flights_clean.parquet") + verificação de roundtrip (ler, assert shape, print file size)                             │ │
│ └─────┴──────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                                                                          │
│ Passo 5: Rodar limpeza.ipynb para gerar data/flights_clean.parquet                                                                                       │
│                                                                                                                                                          │
│ Passo 6: Adicionar data/*.parquet ao .gitignore                                                                                                          │
│                                                                                                                                                          │
│ Passo 7: notebooks/EDA_clean.ipynb                                                                                                                       │
│                                                                                                                                                          │
│ Análise dos dados limpos — insights finais antes da modelagem.                                                                                           │
│                                                                                                                                                          │
│ ┌─────┬──────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐                │
│ │  #  │ Tipo │                                                         Conteúdo                                                         │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 1   │ md   │ Título: "Análise Exploratória — Dados Limpos". Explicar: este notebook parte dos dados já processados por limpeza.ipynb. │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 2   │ code │ Imports + sys.path.insert(0, "..") + from modules.data_loader import load_flights_clean                                  │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 3   │ code │ df = load_flights_clean() — print shape                                                                                  │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 4   │ md   │ Distribuições das features de modelagem: verificar as variáveis que serão usadas.                                        │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 5   │ code │ Histogramas de DEP_HOUR, SEASON, IS_WEEKEND, DISTANCE                                                                    │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 6   │ code │ Balance de IS_DELAYED (82/18) — gráfico de barras + print %                                                              │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 7   │ md   │ Correlações no dataset limpo                                                                                             │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 8   │ code │ Heatmap de correlação (seaborn) com variáveis numéricas de delay                                                         │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 9   │ md   │ Análise por companhia aérea (dados limpos — sem cancelados)                                                              │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 10  │ code │ Avg delay por AIRLINE_NAME + pct_delayed por companhia                                                                   │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 11  │ md   │ Análise geográfica                                                                                                       │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 12  │ code │ Top estados por delay, top aeroportos por delay                                                                          │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 13  │ md   │ Padrões temporais                                                                                                        │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 14  │ code │ Delay por hora, por dia da semana, por mês (tudo sobre dados limpos)                                                     │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 15  │ code │ Causas de atraso: bar chart para voos atrasados                                                                          │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 16  │ md   │ Feature Matrix: construir X e y para verificar shapes antes da modelagem.                                                │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 17  │ code │ Build feature matrix (20 features) + train/test split + print shapes                                                     │                │
│ ├─────┼──────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤                │
│ │ 18  │ md   │ Conclusões e próximos passos: insights, padrões-chave, encaminhar para modelagem.                                        │                │
│ └─────┴──────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘                │
│                                                                                                                                                          │
│ Passo 8: notebooks/modelagem_supervisionada.ipynb                                                                                                        │
│                                                                                                                                                          │
│ ┌─────┬──────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │  #  │ Tipo │                                                                Conteúdo                                                                 │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 1   │ md   │ Título + introdução: dois problemas — classificação (IS_DELAYED) e regressão (DEPARTURE_DELAY).                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2   │ code │ Imports: sklearn (LR, LinearReg, metrics), xgboost, lightgbm, modules                                                                   │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3   │ code │ df = load_flights_clean()                                                                                                               │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 4   │ md   │ Parte 1 — Classificação Binária. IS_DELAYED = (DEPARTURE_DELAY > 15). Imbalance 82/18. Desafio: superar baseline de 82%.                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 5   │ code │ build_classification_split(df) → shapes, class balance                                                                                  │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 6   │ md   │ Modelo 1 — Regressão Logística (baseline). Modelo linear, interpretável, coeficientes = direção/magnitude. solver='saga' para datasets  │ │
│ │     │      │ grandes. class_weight='balanced'.                                                                                                       │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 7   │ code │ Treinar LR. Medir tempo.                                                                                                                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 8   │ code │ Avaliar: classification_report, confusion_matrix, ROC-AUC                                                                               │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 9   │ md   │ Modelo 2 — XGBoost. Gradient boosting: combina árvores fracas iterativamente. Captura não-linearidades e interações.                    │ │
│ │     │      │ scale_pos_weight=4.6 para imbalance. early_stopping_rounds=20.                                                                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 10  │ code │ Treinar XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1, scale_pos_weight=4.6, early_stopping_rounds=20). Eval set = 10% │ │
│ │     │      │  do treino.                                                                                                                             │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 11  │ code │ Avaliar: mesmas métricas                                                                                                                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 12  │ code │ Comparação classificação: tabela lado a lado, ROC curves sobrepostas, feature importance XGBoost                                        │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 13  │ md   │ Análise: qual venceu e por quê. Features mais importantes. Precision vs recall tradeoff.                                                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 14  │ md   │ Parte 2 — Regressão. Prever DEPARTURE_DELAY (minutos) para voos com delay > 0. Problema mais difícil — features pré-partida têm poder   │ │
│ │     │      │ limitado para prever magnitude exata.                                                                                                   │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 15  │ code │ build_regression_split(df) — shapes, target stats                                                                                       │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 16  │ md   │ Modelo 3 — Regressão Linear (baseline). Baseline interpretável.                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 17  │ code │ Treinar e avaliar: MAE, RMSE, R²                                                                                                        │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 18  │ md   │ Modelo 4 — LightGBM Regressor. Histogram-based splitting = 2-3x mais rápido que XGBoost. Ideal para 4.5M rows.                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 19  │ code │ Treinar LGBMRegressor(n_estimators=300, max_depth=6, learning_rate=0.1, early_stopping_rounds=20). Eval set.                            │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 20  │ code │ Avaliar: MAE, RMSE, R², residuals                                                                                                       │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 21  │ md   │ Modelo 5 — XGBoost Regressor. Comparar diretamente com LightGBM: mesmo framework conceitual, implementação diferente.                   │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 22  │ code │ Treinar XGBRegressor (mesmos hiperparâmetros base). Eval set.                                                                           │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 23  │ code │ Avaliar: mesmas métricas                                                                                                                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 24  │ code │ Comparação regressão: tabela 3 modelos, residual plots, feature importance                                                              │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 25  │ md   │ Análise: R² esperado baixo — interpretar significado. LightGBM vs XGBoost: velocidade vs acurácia.                                      │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 26  │ md   │ Conclusões: resumo dos 5 modelos, insights, limitações.                                                                                 │ │
│ └─────┴──────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                                                                          │
│ Passo 9: notebooks/modelagem_nao_supervisionada.ipynb                                                                                                    │
│                                                                                                                                                          │
│ ┌─────┬──────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │  #  │ Tipo │                                                                Conteúdo                                                                 │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 1   │ md   │ Título + introdução: sem labels, buscamos estrutura nos dados.                                                                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2   │ code │ Imports: KMeans, PCA, StandardScaler, modules                                                                                           │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3   │ code │ Carregar dados                                                                                                                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 4   │ md   │ Parte 1 — PCA nas Causas de Atraso. 5 colunas de causa correlacionadas. PCA encontra eixos principais. Filtramos voos atrasados         │ │
│ │     │      │ (IS_DELAYED==1, ~1M rows) — nos demais as 5 colunas são todas 0.                                                                        │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 5   │ code │ Filtrar IS_DELAYED==1. Extrair 5 colunas. StandardScaler.                                                                               │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 6   │ code │ PCA(n_components=5). Scree plot (variância explicada + acumulada).                                                                      │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 7   │ code │ Heatmap dos loadings. Interpretação dos componentes.                                                                                    │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 8   │ code │ Scatter PC1 vs PC2, colorido pela causa dominante.                                                                                      │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │     │      │                                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 9   │ md   │ Parte 2 — K-Means em Perfis de Aeroporto. Pergunta do tech challenge: "É possível agrupar aeroportos com perfis semelhantes?"           │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 10  │ code │ Agregar por ORIGIN_AIRPORT: avg_dep_delay, pct_delayed, avg por causa, total_flights, avg_distance. Filtrar >= 1000 voos.               │ │
│ │     │      │ StandardScaler.                                                                                                                         │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 11  │ code │ Método do Cotovelo + Silhouette Score: KMeans k=2..10.                                                                                  │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 12  │ code │ KMeans com k escolhido. Atribuir labels.                                                                                                │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 13  │ code │ PCA 2D scatter colorido por cluster + bar chart dos centroids.                                                                          │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 14  │ code │ Listar aeroportos por cluster (com nomes). Nomear clusters qualitativamente.                                                            │ │
│ ├─────┼──────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 15  │ md   │ Conclusões: tipologia de aeroportos, padrões de causa, limitações.                                                                      │ │
│ └─────┴──────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                                                                          │
│ Passo 10: notebooks/apresentacao.ipynb                                                                                                                   │
│                                                                                                                                                          │
│ Notebook enxuto para vídeo de 5-10 minutos.                                                                                                              │
│                                                                                                                                                          │
│ ┌─────┬─────────┬───────────────────────────────────────────────────────────────────┐                                                                    │
│ │  #  │  Tipo   │                             Conteúdo                              │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 1   │ md      │ Título, nomes, curso, data                                        │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 2   │ md      │ Agenda                                                            │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 3   │ md+code │ O Dataset + gráfico de balance de classes                         │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 4   │ md+code │ Insights EDA: 2-3 gráficos-chave                                  │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 5   │ md      │ Resultados Classificação: tabela LR vs XGBoost, ROC, top features │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 6   │ md      │ Resultados Regressão: tabela LinReg vs LightGBM vs XGBoost        │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 7   │ md      │ Resultados Não Supervisionados: PCA scree + clusters              │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 8   │ md      │ Limitações                                                        │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 9   │ md      │ Próximos Passos                                                   │                                                                    │
│ ├─────┼─────────┼───────────────────────────────────────────────────────────────────┤                                                                    │
│ │ 10  │ md      │ Conclusão final                                                   │                                                                    │
│ └─────┴─────────┴───────────────────────────────────────────────────────────────────┘                                                                    │
│                                                                                                                                                          │
│ Passo 11: Atualizar CLAUDE.md                                                                                                                            │
│                                                                                                                                                          │
│ ---                                                                                                                                                      │
│ Verificação                                                                                                                                              │
│                                                                                                                                                          │
│ 1. uv sync --group dev instala pyarrow, xgboost, lightgbm sem erros                                                                                      │
│ 2. Rodar EDA_exploratorio.ipynb — sem erros, todas visualizações renderizam                                                                              │
│ 3. Rodar limpeza.ipynb — gera data/flights_clean.parquet, shape ~5.7M × ~36                                                                              │
│ 4. Rodar EDA_clean.ipynb — carrega Parquet, análise completa                                                                                             │
│ 5. Rodar modelagem_supervisionada.ipynb — treina 5 modelos (2 classificação + 3 regressão)                                                               │
│ 6. Rodar modelagem_nao_supervisionada.ipynb — PCA + K-Means executam                                                                                     │
│ 7. Rodar apresentacao.ipynb — todo markdown + gráficos renderizam                                                                                        │
│ 8. import modules.data_loader funciona dos notebooks via sys.path.insert(0, "..")                                                                        │
│                                                                                                                                                          │
│ Riscos e Mitigações                                                                                                                                      │
│                                                                                                                                                          │
│ ┌──────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────┐            │
│ │                Risco                 │                                             Mitigação                                              │            │
│ ├──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤            │
│ │ XGBoost/LightGBM lentos em 4.5M rows │ early_stopping_rounds=20. Se necessário, subsample 2M.                                             │            │
│ ├──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤            │
│ │ LR lento para convergir              │ solver='saga', max_iter=1000                                                                       │            │
│ ├──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤            │
│ │ Classificação fraca (baseline 82%)   │ class_weight='balanced' / scale_pos_weight. Performance limitada é achado válido.                  │            │
│ ├──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤            │
│ │ R² baixo na regressão                │ Esperado — features pré-partida insuficientes para magnitude exata. Achado válido para apresentar. │            │
│ ├──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤            │
│ │ PCA trivial (82% zeros)              │ Filtrar só IS_DELAYED==1 antes do PCA (~1M rows com valores reais).                                │            │
│ ├──────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤            │
│ │ Parquet grande                       │ Compressão snappy → ~200-300MB. Adicionar ao .gitignore.                                           │            │
│ └──────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┘            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────