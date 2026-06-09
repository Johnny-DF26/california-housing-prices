<div align="center">

# California Housing Prices 🏠🇺🇸

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

Análise preditiva utilizando algoritmos de regressão avançados e Machine Learning para estimar o valor mediano de imóveis por quarteirão na Califórnia (Censo de 1990).

</div>

---

## 📜 Entendimento do Negócio e Contexto Histórico
Estamos em outubro de 1990. Você atua como cientista de dados contratado pela **Strategic California Land Partners (SCLP)**, uma firma de investimentos que busca capitalizar sobre a expansão urbana da Costa Oeste. O mercado imobiliário muda rápido demais e os métodos de avaliação tradicionais, baseados no "feeling" de corretores locais, estão falhando.

### 🎯 O Desafio comercial
O Diretor de Aquisições, **Sr. Harrison**, disponibilizou os registros do Censo de 1990 com um ultimato: a firma leva semanas para avaliar o potencial de um distrito habitacional. Se o valor mediano das casas em um bloco for maior do que os fundamentos sugerem, a empresa compra uma bolha. Se for menor, perde uma mina de ouro. 

### 🧹 O Problema Técnico (Os dados reais)
A base apresentava desafios reais de qualidade de dados de campo:
*   Registros ausentes de quantidade de quartos em determinados distritos.
*   Valores de casas de alto luxo "mascarados" ou limitados pelo teto burocrático do governo em \$500.000.
*   Dados de renda codificados de forma não linear.

O objetivo do projeto foi criar um modelo de regressão robusto o suficiente para mitigar esses problemas e prever o `median_house_value`, reduzindo os riscos de falência por supervalorização imobiliária.

---

## 📊 Resumo da Solução e Resultados

O notebook implementa um fluxo completo: análise exploratória (EDA), limpeza, engenharia de features (transformações logarítmicas, one-hot encoding), modelos lineares e de machine learning, validação cruzada e tuning bayesiano.

Abaixo está o comparativo de performance obtido entre os algoritmos testados:

| Modelo | R² (Explicação da Variância) | MAE (Erro Médio Absoluto) |
| :--- | :---: | :---: |
| OLS (Baseline Linear) | 0.664 | ~\$50,000 |
| Random Forest (Baseline) | 0.816 | \$32,068 |
| HistGradientBoosting | 0.827 | - |
| XGBoost (Baseline) | 0.829 | \$31,503 |
| **XGBoost (Otimizado)** | **0.833** | **\$31,079** |

*Conclusão*: O modelo **XGBoost otimizado** entregou o melhor desempenho econômico para a empresa, reduzindo o erro médio por avaliação de imóvel em **~38%** em relação ao modelo linear tradicional (OLS).

### ⚙️ Hiperparâmetros do XGBoost Vencedor
*   `n_estimators`: 107 | `max_depth`: 8 | `learning_rate`: 0.0884
*   `min_child_weight`: 4 | `colsample_bytree`: 0.70 | `subsample`: 0.707

---

## 🛠️ Decisões de Engenharia de Dados (Pré-processamento)
*   **Tratamento de Nulos**: Remoção analítica de registros vazios (~1% da base).
*   **Correção de Assimetria**: Aplicação de transformações logarítmicas em variáveis altamente assimétricas (`total_rooms`, `total_bedrooms`, `population`, `households`, `median_income`, `housing_median_age`, `median_house_value`).
*   **Codificação Categórica**: Uso de *One-hot encoding* para converter a variável explicativa `ocean_proximity`.
*   **Padronização**: Integração de `StandardScaler` diretamente nas pipelines de execução.

---

## 📁 Estrutura do Repositório
```text
├── data/          <- Dados originais (housing.csv) e bases processadas (data.csv)
├── notebooks/     <- Análise exploratória (EDA), pipelines de treino e tuning (.ipynb)
├── models/        <- Modelos treinados salvos em binário para produção
├── docs/          <- Documentação e relatórios executivos de insights
└── requirements.txt <- Arquivo de dependências para replicação do ambiente
```

---

## 🚀 Como Reproduzir (Ambiente Local)

1. **Crie e ative o ambiente virtual (Windows - PowerShell):**
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& ".venv\Scripts\Activate.ps1"
```

2. **Instale as dependências do projeto:**
```bash
pip install -r requirements.txt
```

3. **Execute a análise:**
Abra o arquivo `notebooks/California_Housing_Prices.ipynb` no seu editor ou Jupyter Notebook e execute as células.

---

## 🚧 Próximos Passos
*   [ ] Desenvolvimento de uma interface web no **Streamlit** para permitir que investidores simulem coordenadas geográficas (latitude/longitude) e recebam o preço do imóvel em tempo real.

---

## 📬 Contato e Conexões
*   **Desenvolvedor**: Johnny
*   **LinkedIn**: [in/datasciencejohnny](https://linkedin.com)
*   **E-mail**: johnny.live26@gmail.com
