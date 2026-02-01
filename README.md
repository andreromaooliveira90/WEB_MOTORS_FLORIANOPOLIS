# 🚗 Clusterização Automotiva: Análise Estratégica do Mercado de Carros Usados em Florianópolis/SC

Este projeto realiza uma análise estratégica do mercado de veículos usados em Florianópolis/SC a partir de dados reais coletados via **web scraping** no portal Webmotors. O objetivo é transformar anúncios brutos em **inteligência de mercado**, apoiando decisões de troca de veículo, posicionamento de preço e análise de depreciação.

---

## 🎯 Objetivo

*   Construir uma base de dados própria de anúncios de veículos usados.
*   Identificar regimes reais de mercado com base em preço, quilometragem e idade.
*   Segmentar o mercado em clusters estatisticamente consistentes.
*   Apoiar decisões de investimento e troca de veículos com base em dados.

---

## 🛠️ Engenharia de Dados: Web Scraping

Diferente de projetos baseados em datasets prontos, este trabalho iniciou com a extração automatizada de dados diretamente do portal Webmotors.

*   **Coleta de Dados:** Extração via API interna do site, garantindo dados atualizados da região de Florianópolis.
*   **Superação de Segurança (Anti-Bot):** O portal utiliza mecanismos de proteção como **Click & Hold**. O scraping foi viabilizado por meio de engenharia de requisições HTTP, manipulação dinâmica de headers e gestão de cookies de sessão.
*   **Segurança da Informação:** Cookies e URLs sensíveis foram externalizados em variáveis de ambiente (`.env`), seguindo boas práticas de segurança e versionamento.

---

## 🔬 Processo Analítico

O rigor metodológico foi aplicado em todas as etapas:

*   **Feature Engineering:** Cálculo da idade real dos veículos e categorização mercadológica de marcas (Luxo, Emergente, Volume).
*   **Análise Descritiva:** Avaliação de dispersão (STD) e concentração de preços, identificando assimetrias e regimes de mercado.
*   **Modelagem Estatística:** Clusterização com K-Means, validação via Elbow Method e Silhouette Score, além de testes de estabilidade com múltiplas seeds.

---

## 📊 Resultados da Modelagem: Segmentação de Mercado

O modelo identificou **3 regimes naturais** no mercado de Florianópolis:

| Cluster | Perfil de Mercado | Preço Mediano | KM Mediana | Idade Mediana |
| :--- | :--- | :--- | :--- | :--- |
| **0** | Veteranos / Entrada | R$ 71.900 | 120.194 km | 11 anos |
| **1** | Miolo do Mercado (Seminovos) | R$ 124.900 | 48.233 km | 3 anos |
| **2** | Luxo e Alta Performance | R$ 599.000 | 14.700 km | 3 anos |

---

## 💡 Insights Estratégicos

*   **Convergência de Luxo:** O Cluster 2 apresentou ~98% de pureza estatística em marcas de luxo, validando o posicionamento de preço e a baixa elasticidade do segmento.
*   **Gap de Ascensão:** Para migrar do Cluster 0 para o Cluster 1, o mercado exige um aporte médio entre **R$ 50k e R$ 60k**.
*   **Estabilidade do Modelo:** A consistência dos resultados em múltiplas inicializações confirma que os clusters representam estruturas reais do mercado.

---

## 💻 Tecnologias Utilizadas

*   **Linguagem:** Python 3.x
*   **Processamento de Dados:** Pandas, NumPy
*   **Machine Learning:** Scikit-Learn (StandardScaler, KMeans, Metrics)
*   **Infra & Segurança:** python-dotenv

---

## 📁 Estrutura do Projeto

```text
WEB_MOTORS_FLORIANOPOLIS/
├── config/               # Configurações e parâmetros
├── data/                 # Dados coletados (raw / processed)
├── notebooks/            # Análises exploratórias
├── scripts/              # Scraper e scripts de processamento
├── README.md
└── requirements.txt
