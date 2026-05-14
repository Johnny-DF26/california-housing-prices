# California Housing Prices

Um projeto de ciência de dados que analisa o conjunto de dados de habitação da Califórnia (censo de 1990) e entrega um modelo preditivo para estimar o valor mediano de casas por quarteirão.

## Entendimento do Negócio
### **📜Contexto Histórico**  
Estamos em outubro de 1990. Você como cientista de dados foi contratado pela **Strategic California Land Partners (SCLP)**, uma firma de investimentos que busca capitalizar sobre a expansão urbana da Costa Oeste.O clima no escritório de San Francisco é tenso. O mercado imobiliário está mudando rápido demais e os métodos de avaliação tradicionais, baseados em "feeling" de corretores locais, estão falhando. A diretoria da SCLP tomou uma decisão radical: eles vão ignorar as opiniões dos especialistas e apostar tudo em modelagem ciência de dados.  

### **O Conflito**  
O Diretor de Aquisições, **Sr. Harrison**, entrega a você os dados contendo os registros do Censo de 1990. Ele é direto: "Nós temos bilhões de dólares em capital de investidores. Atualmente, levamos semanas para avaliar o potencial de um distrito habitacional. Se o valor mediano das casas em um bloco for maior do que os fundamentos sugerem, estamos comprando uma bolha. Se for menor, estamos perdendo uma mina de ouro. Eu preciso de uma análise e previsão dessas casas.

### **🧹O Problema Técnico** (A "Sujeira" no Caminho)  
Harrison sabe que os dados são traiçoeiros. Ele avisa que a equipe de campo foi negligente: Existem distritos onde ninguém sabe quantos quartos existem de fato, deixando buracos nos registros.Há uma suspeita de que os valores das casas mais luxuosas foram "mascarados" ou limitados nos relatórios do governo por questões burocráticas, o que pode enganar o seu cálculo.Os números de renda parecem estranhos, codificados de uma forma que só faz sentido para os burocratas do Censo. Sua tarefa é mergulhar nesses dados brutos e construir uma arquitetura de predição. Você deve ser capaz de receber as coordenadas de latitude e longitude, a idade das construções e o perfil econômico daquelas famílias e, como um oráculo, dizer exatamente: "Neste quarteirão, o valor mediano das casas deveria ser X dólares".  
Se o seu modelo de regressão for preciso, a SCLP dominará o mercado imobiliário. Se você falhar e o modelo ignorar as nuances da proximidade com o oceano ou a densidade populacional, a firma enfrentará a falência por pagar caro demais em regiões desvalorizadas.

### **💾 Conteúdo**  
Os dados referem-se às casas encontradas em um determinado distrito da Califórnia e a algumas estatísticas resumidas sobre elas com base nos dados do censo de 1990. Atenção: os dados não estão limpos, portanto, algumas etapas de pré-processamento são necessárias! As colunas são as seguintes, e seus nomes são bastante autoexplicativos:

* **longitude:** uma medida que indica a distância a oeste de uma casa; quanto maior o valor, mais a oeste ela fica
* **latitude:** Uma medida que indica a latitude de uma casa; quanto maior o valor, mais ao norte ela fica
* **housing_median_age:** Idade média das casas de um quarteirão; um número mais baixo indica que se trata de um prédio mais novo
* **total_rooms:** Número total de quartos em um bloco
* **total_bedrooms:** Número total de quartos em um prédio
* **population:** Número total de pessoas que residem em um quarteirão
* **households:** Número total de famílias, ou seja, grupos de pessoas que residem em uma unidade habitacional, para um quarteirão
* **median_income:** Renda média das famílias em um quarteirão (medida em dezenas de milhares de dólares americanos)
* **median_house_value:** Valor mediano das casas para as famílias de um quarteirão (medido em dólares americanos)
* **ocean_proximity:** Localização da casa em relação ao oceano/mar

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
