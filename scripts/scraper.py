

import httpx
import pandas as pd
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()  # carrega o .env da raiz do projeto (diretório atual)

meu_cookie = os.getenv("WEBMOTORS_COOKIE")
if not meu_cookie:
    raise ValueError("WEBMOTORS_COOKIE não encontrado. Verifique o arquivo .env na raiz do projeto.")

URL_TEMPLATE = os.getenv("WEBMOTORS_API_URL_TEMPLATE")
if not URL_TEMPLATE:
    raise ValueError("WEBMOTORS_API_URL_TEMPLATE não encontrado no .env")

def extrair_webmotors_ate_o_fim():
    diretorio_destino = r"C:\Users\aoliveira_esss\Documents\WEB_MOTORS_FLORIANOPOLIS\data\raw"
    if not os.path.exists(diretorio_destino): os.makedirs(diretorio_destino)
    
    headers = {
        "authority": "www.webmotors.com.br",
        "accept": "application/json, text/plain, */*",
        "cookie": meu_cookie,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    todos_veiculos = []
    pagina_atual = 1
    ha_mais_paginas = True

    with httpx.Client(headers=headers, http2=True) as client:
        while ha_mais_paginas:
            print(f"Processando página {pagina_atual}...")
            
            # URL da API
            url = URL_TEMPLATE.format(page=pagina_atual)

            try:
                response = client.get(url, timeout=25)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('SearchResults', [])
                    
                    # SE A PÁGINA VIER VAZIA, PARAMOS O LOOP
                    if not results or len(results) == 0:
                        print(f"Página {pagina_atual} está vazia. Fim da extração.")
                        ha_mais_paginas = False
                        break

                    for carro in results:
                        spec = carro.get('Specification', {})
                        seller = carro.get('Seller', {})
                        prices = carro.get('Prices', {})
                        
                        attrs = ", ".join([a.get('Name') for a in spec.get('VehicleAttributes', []) if isinstance(a, dict)])

                        todos_veiculos.append({
                            "Titulo": spec.get('Title'),
                            "Marca": spec.get('Make', {}).get('Value'),
                            "Modelo": spec.get('Model', {}).get('Value'),
                            "Versao": spec.get('Version', {}).get('Value'),
                            "Ano_Fab": spec.get('YearFabrication'),
                            "Ano_Mod": spec.get('YearModel'),
                            "Quilometragem": spec.get('Odometer'),
                            "Cambio": spec.get('Transmission'),
                            "Portas": spec.get('NumberPorts'),
                            "Tipo_Carroceria": spec.get('BodyType'),
                            "Cor": spec.get('Color', {}).get('Primary'),
                            "Preco": prices.get('Price'),
                            "Cidade": seller.get('City'),
                            "Vendedor": seller.get('FantasyName') or "Particular",
                            "Atributos": attrs,
                            "Descricao": str(carro.get('LongComment', '')).replace('\n', ' ').replace('\r', ' ').replace(';', ','),
                            "Link": f"https://www.webmotors.com.br/comprar/{carro.get('UniqueId')}"
                        })
                    
                    print(f"Página {pagina_atual} concluída. {len(results)} veículos capturados.")
                    pagina_atual += 1
                    
                    # Pausa para segurança (evitar 403)
                    time.sleep(random.uniform(2.0, 4.0))
                
                elif response.status_code == 403:
                    print("Erro 403: O Cookie expirou ou o IP foi bloqueado.")
                    ha_mais_paginas = False
                else:
                    print(f"Erro inesperado na página {pagina_atual}: {response.status_code}")
                    ha_mais_paginas = False

            except Exception as e:
                print(f"Erro técnico na página {pagina_atual}: {e}")
                ha_mais_paginas = False

    if todos_veiculos:
        df = pd.DataFrame(todos_veiculos)
        
        # Limpeza rigorosa para o Excel não quebrar
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.replace(r'[\n\r\t]', ' ', regex=True).str.replace(';', ',')
            
        caminho_final = os.path.join(diretorio_destino, "base_floripa_completa.csv")
        df.to_csv(caminho_final, index=False, sep=';', encoding="utf-8-sig")
        
        print(f"\n--- SUCESSO TOTAL ---")
        print(f"Total de veículos extraídos: {len(todos_veiculos)}")
        print(f"Arquivo salvo em: {caminho_final}")

if __name__ == "__main__":
    extrair_webmotors_ate_o_fim()