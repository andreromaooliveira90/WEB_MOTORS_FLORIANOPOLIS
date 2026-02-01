
🚗 Clusterização Automotiva: Análise Estratégica do Mercado de Carros Usados em Florianópolis/SC

Este projeto realiza uma análise estratégica do mercado de veículos usados em Florianópolis/SC a partir de dados reais coletados via web scraping no portal Webmotors.
O objetivo é transformar anúncios brutos em inteligência de mercado, apoiando decisões de troca de veículo, posicionamento de preço e análise de depreciação.

🎯 Objetivo
Construir uma base de dados própria de anúncios de veículos usados.
Identificar regimes reais de mercado com base em preço, quilometragem e idade.
Segmentar o mercado em clusters estatisticamente consistentes.
Apoiar decisões de investimento e troca de veículos com base em dados.
🛠️ Engenharia de Dados: Web Scraping

Diferente de projetos baseados em datasets prontos, este trabalho iniciou com a extração automatizada de dados diretamente do portal Webmotors.

Coleta de Dados:
Extração via API interna do site, garantindo dados atualizados da região de Florianópolis.

Superação de Segurança (Anti-Bot):
O portal utiliza mecanismos de proteção como Click & Hold.
O scraping foi viabilizado por meio de:

Engenharia de requisições HTTP
Manipulação dinâmica de headers
Gestão de cookies de sessão

Segurança da Informação:
Cookies e URLs sensíveis foram externalizados em variáveis de ambiente (.env), seguindo boas práticas de segurança e versionamento.

🔬 Processo Analítico

O rigor metodológico foi aplicado em todas as etapas:

Feature Engineering

Cálculo da idade real dos veículos
Categorização mercadológica de marcas (Luxo, Emergente, Volume)

Análise Descritiva

Avaliação de dispersão (STD) e concentração de preços
Identificação de assimetrias e regimes de mercado

Modelagem Estatística

Clusterização com K-Means
Validação via Elbow Method e Silhouette Score
Testes de estabilidade com múltiplas seeds
📊 Resultados da Modelagem: Segmentação de Mercado

O modelo identificou 3 regimes naturais no mercado de Florianópolis:

Cluster	Perfil de Mercado	Preço Mediano	KM Mediana	Idade Mediana
0	Veteranos / Entrada	R$ 71.900	120.194 km	11 anos
1	Miolo do Mercado (Seminovos)	R$ 124.900	48.233 km	3 anos
2	Luxo e Alta Performance	R$ 599.000	14.700 km	3 anos
💡 Insights Estratégicos

Convergência de Luxo:
O Cluster 2 apresentou ~98% de pureza estatística em marcas de luxo, validando o posicionamento de preço e a baixa elasticidade do segmento.

Gap de Ascensão:
Para migrar do Cluster 0 para o Cluster 1, o mercado exige um aporte médio entre R50keR 60k, o que fundamenta decisões de troca de veículo.

Estabilidade do Modelo:
A consistência dos resultados em múltiplas inicializações confirma que os clusters representam estruturas reais do mercado.

💻 Tecnologias Utilizadas
Linguagem: Python 3.x
Processamento de Dados: Pandas, NumPy
Machine Learning: Scikit-Learn (StandardScaler, KMeans, Metrics)
Infra & Segurança: python-dotenv (gestão de segredos)
📁 Estrutura do Projeto
WEB_MOTORS_FLORIANOPOLIS/
│
├── .github/              # Configurações de CI/CD (se aplicável)
├── config/               # Configurações e parâmetros
├── data/                 # Dados coletados (raw / processed)
├── notebooks/            # Análises exploratórias
├── perfil_webmotors/     # Outputs analíticos
├── scripts/              # Scraper e scripts de processamento
├── venv/                 # Ambiente virtual (ignorado no Git)
├── README.md
├── requirements.txt
└── .gitignore

▶️ Como Executar
Clone o repositório.
Crie o ambiente virtual:
python -m venv venv

Ative o ambiente e instale as dependências:
pip install -r requirements.txt

Crie o arquivo .env com as variáveis necessárias.
Execute o scraper:
python scripts/scraper.py


Autor:
André Oliveira
Data Science • Market Intelligence • Analytics

✅ O que este README agora entrega
Padronização visual com seus outros projetos
Clareza técnica sem excesso de marketing
Demonstração explícita de engenharia + ciência de dados
Narrativa end-to-end (scraping → modelagem → decisão)

Se quiser, no próximo passo posso:

revisar o README linha a linha como se fosse code review, ou
ajustar o tom (mais acadêmico / mais business / mais recrutador).