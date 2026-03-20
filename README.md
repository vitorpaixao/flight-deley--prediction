# Flight Delay Prediction

Projeto de previsao de atrasos de voos utilizando o dataset "Flight Delays and Cancellations" do US DOT (2015, ~5.8M registros). Trabalho academico da pos-graduacao (Fase 3: Machine Learning Engineering).

## Pre-requisitos

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes e ambientes virtuais)

## Instalacao do uv

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux / macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Apos a instalacao, reinicie o terminal e verifique:

```bash
uv --version
```

## Configuracao do ambiente

### 1. Instalar dependencias do projeto

```bash
uv sync --group dev
```

Isso cria o ambiente virtual (`.venv/`) e instala todas as dependencias do projeto (pandas, numpy, matplotlib) junto com as de desenvolvimento (JupyterLab, ipykernel).

### 2. Adicionar novas dependencias ao projeto

Para adicionar uma dependencia principal:

```bash
uv add nome-do-pacote
```

Para adicionar uma dependencia de desenvolvimento (como o JupyterLab):

```bash
uv add --group dev nome-do-pacote
```

Exemplos usados neste projeto:

```bash
uv add pandas numpy matplotlib
uv add --group dev jupyterlab ipykernel
```

Apos adicionar, sincronize o ambiente:

```bash
uv sync --group dev
```

### 2. Registrar o kernel do Jupyter

```bash
uv run python -m ipykernel install --user --name flight-delay-prediction --display-name "Flight Delay Prediction"
```

Isso registra o Python do `.venv` como um kernel do Jupyter, garantindo que os notebooks tenham acesso a todas as dependencias do projeto.

### 3. Iniciar o JupyterLab

```bash
uv run jupyter lab
```

### 4. Abrir e executar o notebook

1. No JupyterLab, abra `notebooks/eda_flights.ipynb`
2. Selecione o kernel **"Flight Delay Prediction"** (menu Kernel > Change Kernel)
3. Execute as celulas normalmente

## Executar scripts

Os scripts em `src/` devem ser executados a partir da raiz do projeto:

```bash
uv run python src/data_analisys/flights_drops.py
```

## Dados

Os arquivos CSV devem estar em `data/`:

- `flights.csv` — registros de voos (~5.8M linhas)
- `airports.csv` — metadados dos aeroportos
- `airlines.csv` — codigos das companhias aereas

O dicionario de dados esta em `plan/dic_data.md`.

## Estrutura do projeto

```
flight-delay-prediction/
├── data/                  # CSVs do dataset
├── notebooks/             # Notebooks de analise e modelagem
├── src/data_analisys/     # Scripts de exploracao de dados
├── plan/                  # Documentacao e planejamento
├── main.py                # Ponto de entrada
└── pyproject.toml         # Dependencias do projeto
```
