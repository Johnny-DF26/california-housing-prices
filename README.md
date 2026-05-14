# California Housing Prices

Um projeto de ciência de dados que analisa o conjunto de dados de habitação da Califórnia (censo de 1990) e entrega um modelo preditivo para estimar o valor mediano de casas por quarteirão.

## Sumário
- **Objetivo:** prever `median_house_value` (valor mediano das casas) por quarteirão e entregar um modelo robusto para suporte a decisões de investimento.
- **Dados principais:** `data/housing.csv` (versão original) e `data.csv` (versões processadas/derivadas).
- **Notebook principal:** [notebooks/California_Housing_Prices.ipynb](notebooks/California_Housing_Prices.ipynb)
- **Dependências:** [requirements.txt](requirements.txt)

## Estrutura do repositório

- `data/` — dados brutos e processados.
- `notebooks/` — análise exploratória, pipelines, tuning e relatório (`California_Housing_Prices.ipynb`).
- `models/` — modelos treinados e artefatos (quando gerados).
- `docs/` — documentação e resultados resumidos.
- `requirements.txt` — dependências Python para reproduzir o ambiente.

## Resumo da solução

O notebook implementa um fluxo completo: análise exploratória (EDA), limpeza, engenharia de features (transformações logarítmicas, one-hot encoding), modelos lineares e de machine learning, validação cruzada e tuning bayesiano. Resultados consolidados:

| Modelo | R² (aprox.) | MAE (aprox.) |
| :--- | :---: | :---: |
| OLS (baseline) | 0.664 | ~$50,000 |
| Random Forest (baseline) | 0.816 | $32,068 |
| XGBoost (baseline) | 0.829 | $31,503 |
| XGBoost (otimizado) | **0.833** | **$31,079** |

Conclusão: o melhor desempenho foi alcançado com o `XGBoost` otimizado (maior R² e menor MAE). Modelos adicionais testados: Random Forest tunado (R² ≈ 0.813) e HistGradientBoosting (R² ≈ 0.827).

### Hiperparâmetros do XGBoost (melhor configuração usada no notebook)

- `n_estimators`: 107
- `max_depth`: 8
- `learning_rate`: 0.0884
- `min_child_weight`: 4
- `colsample_bytree`: 0.70
- `subsample`: 0.707

## Principais decisões de pré-processamento

- Remoção de registros com valores nulos (≈1% da base).
- Transformações logarítmicas em variáveis com forte assimetria (`total_rooms`, `total_bedrooms`, `population`, `households`, `median_income`, `housing_median_age`, `median_house_value`).
- One-hot encoding para `ocean_proximity` (categorias que capturam proximidade ao mar).
- Padronização (StandardScaler) aplicada quando indicado pelo pipeline.
- Atenção com viés de censura em `median_house_value` (teto em $500.000) — tratado/avaliado na EDA e nos modelos.

## Recomendações de negócio (resumo executivo)

- `median_income` e proximidade ao oceano são os preditores mais fortes; priorizar áreas com renda média elevada e proximidade costeira.
- A categoria `ISLAND` apresenta alto coeficiente, mas baixa representatividade (apenas 5 registros) — não tomar decisões de alto impacto baseadas apenas nessa categoria sem coleta adicional.
- O modelo XGBoost otimizado reduz o erro médio por avaliação em ~38% em relação ao OLS, tornando-o a escolha recomendada para suporte a decisões de compra/valorização.

## Como reproduzir (ambiente local)

1. Criar e ativar ambiente virtual (Windows - PowerShell):

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& ".venv\Scripts\Activate.ps1"
```

2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Executar o notebook:

- Abra [notebooks/California_Housing_Prices.ipynb](notebooks/California_Housing_Prices.ipynb) em Jupyter ou VS Code e execute as células na ordem apresentada.

4. Resultado e artefatos:

- O notebook treina modelos, executa validação cruzada e mostra comparativos. Salve artefatos em `models/` usando `joblib` ou `pickle` caso queira promover o modelo para produção.

## Arquivos importantes

- Notebook: [notebooks/California_Housing_Prices.ipynb](notebooks/California_Housing_Prices.ipynb)
- Dados: [data/housing.csv](data/housing.csv) (original) e [data/data.csv](data/data.csv) (derivado)
- Dependências: [requirements.txt](requirements.txt)
- Modelos (esperado): [models/](models/)

## Licença

Este repositório não possui licença explícita; adicione um arquivo LICENSE caso deseje especificar os termos de uso.

## Contato

Abra uma issue para dúvidas, solicitações de melhoria ou pedido de integração.
