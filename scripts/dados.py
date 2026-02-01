import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings

# Supressão de avisos de depreciação para manter o console limpo
warnings.filterwarnings("ignore", category=FutureWarning)

# ==============================================================================
# CONFIGURAÇÕES E CONSTANTES
# ==============================================================================
PATH_BRUTO = r"C:\Users\aoliveira_esss\Documents\WEB_MOTORS_FLORIANOPOLIS\data\raw\base_floripa_completa.csv"
ANO_BASE = 2025

MARCAS_LUXO = [
    'BMW', 'MERCEDES-BENZ', 'LAND ROVER', 'PORSCHE', 'AUDI', 'RAM', 'VOLVO', 
    'MINI', 'ZEEKR', 'JAGUAR', 'JEEP', 'LEXUS', 'DODGE', 'MASERATI', 
    'ASTON MARTIN', 'FERRARI', 'TESLA', 'INFINITI'
]

MARCAS_EMERGENTES = [
    'BYD', 'GWM', 'MG', 'CAOA CHERY', 'JAECOO', 'OMODA', 'LEAPMOTOR'
]

GRUPOS_FOCO = [
    ('Luxo', 'Utilitário esportivo'),
    ('Volume', 'Utilitário esportivo'),
    ('Volume', 'Hatchback'),
    ('Volume', 'Picape'),
    ('Volume', 'Sedã')
]

# ==============================================================================
# FUNÇÕES AUXILIARES DE FORMATAÇÃO
# ==============================================================================
def fmt_real(x):
    if pd.isna(x): return ""
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_int(x):
    if pd.isna(x): return ""
    return f"{x:,.0f}".replace(",", ".")

def fmt_perc(x):
    if pd.isna(x): return ""
    return f"{x:.2f}%".replace(".", ",")

# ==============================================================================
# ETAPA 1: CLASSIFICAÇÃO E ENGENHARIA DE ATRIBUTOS
# ==============================================================================
def classificar_categoria(marca):
    """Classifica marca em Luxo, Emergente ou Volume."""
    if marca in MARCAS_LUXO: return 'Luxo'
    if marca in MARCAS_EMERGENTES: return 'Emergente'
    return 'Volume'

# ==============================================================================
# ETAPA 2: CARGA E PREPARAÇÃO DO DATASET
# ==============================================================================
def preparar_dataset(path):
    """Carrega, limpa e prepara o dataset de veículos usados."""
    print("\n=== ETAPA 1: CARREGAMENTO E PREPARAÇÃO DOS DADOS ===")
    
    df = pd.read_csv(path, sep=';', encoding='utf-8-sig')
    df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce')
    df['Quilometragem'] = pd.to_numeric(df['Quilometragem'], errors='coerce')
    df['Ano_Mod'] = df['Ano_Mod'].fillna(0).astype(int)
    df['Categoria'] = df['Marca'].apply(classificar_categoria)
    df['Estado'] = np.where(df['Quilometragem'] <= 0, 'Novo', 'Usado')
    df['Idade'] = ANO_BASE - df['Ano_Mod']
    
    df_usados = df[(df['Estado'] == 'Usado') & (df['Preco'] > 5000)].copy()
    
    print(f"✓ Total de registros carregados: {len(df):,}".replace(",", "."))
    print(f"✓ Veículos usados (Preço > R$ 5.000): {len(df_usados):,}".replace(",", "."))
    print(f"✓ Período analisado: {df_usados['Ano_Mod'].min()} a {df_usados['Ano_Mod'].max()}")
    
    return df_usados

# ==============================================================================
# ETAPA 3: ANÁLISE ESTATÍSTICA DESCRITIVA
# ==============================================================================
def analisar_estatistica_descritiva(df):
    """Gera estatísticas descritivas por Categoria e Tipo de Carroceria."""
    print("\n=== ETAPA 2: ESTATÍSTICA DESCRITIVA POR CATEGORIA E CARROCERIA ===")
    stats = df.groupby(['Categoria', 'Tipo_Carroceria'])['Preco'].describe()
    
    for metrica in ['count', 'mean', '50%', 'std']:
        print(f"\n>>> TABELA: {metrica.upper()}")
        tabela = stats[metrica].unstack(level=0).fillna(0)
        
        if 'Volume' in tabela.columns:
            tabela = tabela.sort_values(by='Volume', ascending=False)
        
        ordem = [c for c in ['Volume', 'Luxo', 'Emergente'] if c in tabela.columns]
        tabela = tabela[ordem]

        if metrica == 'count':
            print(tabela.astype(int))
        else:
            print(tabela.applymap(fmt_real))

# ==============================================================================
# ETAPA 4: ANÁLISE DE COBERTURA (MÉDIA ± k*STD)
# ==============================================================================
def analisar_cobertura_std(df, ks=(1, 2)):
    """Calcula percentual de dados dentro de média ± k*STD."""
    print("\n=== ETAPA 3: RELATÓRIO DE COBERTURA (MÉDIA ± k*STD) ===")
    grupos = df.groupby(['Categoria', 'Tipo_Carroceria']).size().reset_index()
    
    for k in ks:
        print(f"\n>>> RESULTADOS PARA k={k}")
        linhas = []
        for _, row in grupos.iterrows():
            cat, carr = row['Categoria'], row['Tipo_Carroceria']
            recorte = df[(df['Categoria'] == cat) & (df['Tipo_Carroceria'] == carr)]['Preco']
            
            if len(recorte) > 0:
                m, s = recorte.mean(), recorte.std()
                dentro = recorte.between(m - k*s, m + k*s).sum()
                linhas.append({
                    'Categoria': cat, 'Carroceria': carr, 'n': len(recorte),
                    'media': fmt_real(m), 'std': fmt_real(s), 
                    'perc_dentro': fmt_perc(100 * dentro / len(recorte))
                })
        
        rel = pd.DataFrame(linhas).sort_values('n', ascending=False)
        print(rel.to_string(index=False))

# ==============================================================================
# ETAPA 5: PERFIL MEDIANO DOS 5 MAIORES GRUPOS
# ==============================================================================
def analisar_perfil_grupos_foco(df):
    """Analisa perfil mediano (Preço, KM, Idade) dos grupos foco."""
    print("\n=== ETAPA 4: PERFIL MEDIANO DOS 5 MAIORES GRUPOS (IDADE E KM) ===")
    
    resultados = []
    for cat, carr in GRUPOS_FOCO:
        df_g = df[(df['Categoria'] == cat) & (df['Tipo_Carroceria'] == carr)]
        if len(df_g) > 0:
            resultados.append({
                'Categoria': cat,
                'Carroceria': carr,
                'n': len(df_g),
                'Preco_Med': fmt_real(df_g['Preco'].median()),
                'KM_Med': fmt_int(df_g['Quilometragem'].median()),
                'Ano_Med': int(df_g['Ano_Mod'].median()),
                'Idade_Med': int(df_g['Idade'].median())
            })
    
    print(pd.DataFrame(resultados).to_string(index=False))

# ==============================================================================
# ETAPA 6: ANÁLISE DETALHADA POR MODELO (TOP 5)
# ==============================================================================
def analisar_perfil_modelos(df):
    """Analisa perfil dos Top 5 modelos de cada grupo foco."""
    print("\n=== ETAPA 5: PERFIL DETALHADO POR MODELO (TOP 5 DE CADA GRUPO) ===")
    
    for cat, carr in GRUPOS_FOCO:
        df_g = df[(df['Categoria'] == cat) & (df['Tipo_Carroceria'] == carr)]
        if len(df_g) == 0: continue
        
        top_m = df_g['Modelo'].value_counts().head(5).index
        
        res = []
        for mod in top_m:
            df_m = df_g[df_g['Modelo'] == mod]
            res.append({
                'Modelo': mod, 'n': len(df_m), 
                'Preco_Med': fmt_real(df_m['Preco'].median()),
                'KM_Med': fmt_int(df_m['Quilometragem'].median()),
                'Idade_Med': int(df_m['Idade'].median())
            })
        
        print(f"\n>>> GRUPO: {cat} | {carr}")
        print(pd.DataFrame(res).to_string(index=False))

# ==============================================================================
# ETAPA 7: SENSIBILIDADE AO USO (ISU)
# ==============================================================================
def analisar_sensibilidade_uso(df):
    """Calcula quanto o preço cai a cada 10.000 km rodados."""
    print("\n=== ETAPA 6: SENSIBILIDADE AO USO (QUEDA DE PREÇO A CADA 10k KM) ===")
    
    for cat, carr in GRUPOS_FOCO:
        df_g = df[(df['Categoria'] == cat) & (df['Tipo_Carroceria'] == carr)]
        if len(df_g) == 0: continue
        
        top_m = df_g['Modelo'].value_counts().head(5).index
        
        res = []
        for mod in top_m:
            df_m = df_g[df_g['Modelo'] == mod]
            if len(df_m) < 10: continue
            
            km_c = df_m['Quilometragem'].median()
            p_a = df_m[df_m['Quilometragem'] <= km_c]['Preco'].median()
            p_b = df_m[df_m['Quilometragem'] > km_c]['Preco'].median()
            k_a = df_m[df_m['Quilometragem'] <= km_c]['Quilometragem'].median()
            k_b = df_m[df_m['Quilometragem'] > km_c]['Quilometragem'].median()
            
            isu = ((p_a - p_b) / (k_b - k_a)) * 10000 if (k_b - k_a) > 0 else 0
            res.append({
                'Modelo': mod, 
                'Preco_Med': fmt_real(df_m['Preco'].median()), 
                'ISU_10k': fmt_real(isu)
            })
        
        if res:
            print(f"\n>>> GRUPO: {cat} | {carr}")
            print(pd.DataFrame(res).to_string(index=False))

# ==============================================================================
# ETAPA 8: MODELAGEM DE CLUSTERS (K-MEANS)
# ==============================================================================
def executar_clusterizacao(df):
    """Executa K-Means (k=3) e analisa perfil dos clusters."""
    print("\n=== ETAPA 7: MODELAGEM DE CLUSTERS (K-MEANS) ===")
    
    # Preparação
    df_feat = df[['Preco', 'Quilometragem', 'Idade']].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_feat)
    
    # K-Means Final (k=3)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=20)
    df.loc[df_feat.index, 'Cluster'] = kmeans.fit_predict(X_scaled)
    
    print(f"\n✓ Modelo treinado com {len(df_feat):,} registros".replace(",", "."))
    print(f"✓ Inércia do modelo: {kmeans.inertia_:,.2f}".replace(",", "."))
    
    # Perfil dos Clusters
    perfil = df.dropna(subset=['Cluster']).groupby('Cluster').agg(
        Preco_Med=('Preco', 'median'), 
        KM_Med=('Quilometragem', 'median'),
        Idade_Med=('Idade', 'median'), 
        n=('Preco', 'size')
    ).sort_values('Preco_Med').reset_index()
    
    print("\n>>> PERFIL DOS CLUSTERS:")
    t = perfil.copy()
    t['Preco_Med'] = t['Preco_Med'].apply(fmt_real)
    t['KM_Med'] = t['KM_Med'].apply(fmt_int)
    t['Idade_Med'] = t['Idade_Med'].astype(int)
    print(t.to_string(index=False))
    
    # Cruzamento Categoria
    print("\n>>> CRUZAMENTO: CLUSTER x CATEGORIA (%)")
    cross = pd.crosstab(df.dropna(subset=['Cluster'])['Cluster'], 
                        df.dropna(subset=['Cluster'])['Categoria'], 
                        normalize='index') * 100
    print(cross.round(2).applymap(fmt_perc))
    
    return df

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    # Etapa 1: Carga e Preparação
    df_usados = preparar_dataset(PATH_BRUTO)
    
    # Etapa 2: Estatística Descritiva
    analisar_estatistica_descritiva(df_usados)
    
    # Etapa 3: Cobertura STD
    analisar_cobertura_std(df_usados)
    
    # Etapa 4: Perfil dos Grupos Foco
    analisar_perfil_grupos_foco(df_usados)
    
    # Etapa 5: Perfil por Modelo
    analisar_perfil_modelos(df_usados)
    
    # Etapa 6: Sensibilidade ao Uso
    analisar_sensibilidade_uso(df_usados)
    
    # Etapa 7: Clusterização
    df_final = executar_clusterizacao(df_usados)
    
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA COM SUCESSO")
    print("="*80)

# %%
# %%