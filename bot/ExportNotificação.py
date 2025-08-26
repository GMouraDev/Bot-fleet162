import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from tqdm import tqdm
import tempfile
import shutil
import io

# Carrega as variáveis de ambiente
load_dotenv('config.env')

# Obtém as credenciais e URLs das variáveis de ambiente
login_page_url = os.getenv('FROTA162_LOGIN_URL')
login_url = os.getenv('FROTA162_LOGIN_URL')
export_url = os.getenv('FROTA162_NOTIFICACOES_EXPORT_URL')

username = os.getenv('FROTA162_USERNAME')
password = os.getenv('FROTA162_PASSWORD')

# Verifica se as credenciais foram carregadas
if not username or not password:
    print("Erro: Credenciais não encontradas no arquivo config.env")
    print("Certifique-se de que o arquivo config.env existe e contém FROTA162_USERNAME e FROTA162_PASSWORD")
    exit()

# Verifica e cria a pasta Resources se não existir
resources_dir = "Resources"
if not os.path.exists(resources_dir):
    print(f"Criando pasta {resources_dir}...")
    os.makedirs(resources_dir)
    print(f"Pasta {resources_dir} criada com sucesso!")

print("Iniciando processo de exportação de notificações...")

try:
    session = requests.Session()
    
    print("Acessando página de login...")
    login_page = session.get(login_page_url)
    
    if login_page.status_code != 200:
        raise Exception(f"Erro ao acessar página de login: Status {login_page.status_code}")
    
    soup = BeautifulSoup(login_page.text, 'html.parser')
    
    # Validação do token CSRF
    csrf_input = soup.find('input', {'name': '_token'})
    if not csrf_input:
        raise Exception("Token CSRF não encontrado na página de login. Verifique se o sistema está funcionando.")
    
    csrf_token = csrf_input['value']
    print("Token CSRF capturado com sucesso!")

    login_data = {
        "username": username,
        "password": password,
        "_token": csrf_token
    }

    print("Realizando login...")
    login_response = session.post(login_url, data=login_data)
    
    if login_response.status_code != 200:
        raise Exception(f"Erro ao fazer login: Status {login_response.status_code}")
    
    # Validação simples de login - verifica se foi redirecionado
    if "login" in login_response.url.lower():
        raise Exception("Login falhou - ainda na página de login")
    
    print("Login realizado com sucesso!")

    print("Exportando dados de notificações...")
    export_response = session.get(export_url)
    
    if export_response.status_code != 200:
        raise Exception(f"Erro ao baixar arquivo de exportação: Status {export_response.status_code}")
    
    # Validação do conteúdo da resposta
    if not export_response.content or len(export_response.content) < 100:
        raise Exception("Arquivo de exportação vazio ou muito pequeno")
    
    print("Arquivo de exportação baixado com sucesso!")
    
    # Processa o arquivo em memória
    print("Processando dados...")
    with tqdm(total=100, desc="Processando dados") as pbar:
        pbar.update(20)
        
        # Lê o arquivo diretamente da memória
        new_data = pd.read_excel(io.BytesIO(export_response.content))
        pbar.update(30)
        
        # Validação dos dados
        if new_data.empty:
            raise Exception("Arquivo exportado está vazio")
        
        if "AIT" not in new_data.columns:
            raise Exception("Coluna 'AIT' não encontrada nos dados exportados")
        
        pbar.update(20)
        
        # Verifica se existe arquivo anterior
        try:
            existing_data = pd.read_excel(f"{resources_dir}/Notificacao162.xlsx")
            print(f"Dados existentes carregados: {len(existing_data)} registros")
        except FileNotFoundError:
            existing_data = pd.DataFrame()
            print("Nenhum arquivo anterior encontrado. Criando novo arquivo.")
        
        pbar.update(10)
        
        # Processa e combina dados
        if not existing_data.empty:
            print("Combinando dados existentes com novos dados...")
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
            unique_data = combined_data.drop_duplicates(subset="AIT", keep="first")
            new_entries = unique_data[~unique_data["AIT"].isin(existing_data["AIT"])]
            print(f"Total de registros únicos: {len(unique_data)}")
        else:
            unique_data = new_data
            new_entries = new_data
            print(f"Total de registros: {len(unique_data)}")
        
        pbar.update(20)
        
        # Salva arquivo final
        output_path = f"{resources_dir}/Notificacao162.xlsx"
        unique_data.to_excel(output_path, index=False)
        print(f"Planilha de notificações salva em: {output_path}")
        
        pbar.update(100)
    
    print(f"✅ Processo concluído! Novas notificações importadas: {len(new_entries)}")
    print(f"📊 Total de registros únicos: {len(unique_data)}")

except Exception as e:
    print(f"❌ Erro durante o processo: {str(e)}")
    print(f"🔍 Detalhes do erro: {type(e).__name__}")
    exit(1)
except KeyboardInterrupt:
    print("\n⚠️ Processo interrompido pelo usuário")
    exit(1)

