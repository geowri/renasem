import argparse
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do argumento de linha de comando
parser = argparse.ArgumentParser(description="Extrair dados do RENASEM para o estado especificado.")
parser.add_argument("estado", help="Código do estado (ex: PA, SP, RJ)")
args = parser.parse_args()

# Configuração do navegador
driver = webdriver.Chrome()  # ou use webdriver.Firefox() se preferir
url = "https://sistemasweb.agricultura.gov.br/renasem/psq_consultarenasems.do"
driver.get(url)

# Espera até que a página carregue o seletor de estado
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.NAME, "valor(sgUf)")))

# Seleciona o estado informado no argumento
estado_select = Select(driver.find_element(By.NAME, "valor(sgUf)"))
estado_select.select_by_value(args.estado)

# Clica no botão de pesquisa
pesquisar_button = driver.find_element(By.ID, "botaoPesquisar")
pesquisar_button.click()

# Lista para armazenar os dados extraídos
dados = []

# Função para extrair dados da página atual
def extrair_dados_pagina():
    linhas = driver.find_elements(By.XPATH, "//tr[contains(@bgcolor, '#eeffee') or contains(@bgcolor, '#FFFFFF')]")
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if len(colunas) >= 9:
            dados.append({
                "UF": colunas[0].text,
                "Município": colunas[1].text,
                "Renasem": colunas[2].text,
                "Validade": colunas[3].text,
                "Atividade": colunas[4].text,
                "CPF/CNPJ": colunas[5].text,
                "Nome": colunas[6].text,
                "Endereço": colunas[7].text,
                "Cep": colunas[8].text
            })

# Extrair dados da primeira página
extrair_dados_pagina()

# Navegar pelas páginas
while True:
    try:
        # Verifica se o botão "Próximo" está ativo
        proximo_button = driver.find_element(By.XPATH, "//img[@title='Próximo']")
        if "off" in proximo_button.get_attribute("src"):  # Verifica se o botão está desativado
            break

        # Clica no botão "Próximo" e espera a página carregar
        proximo_button.click()
        time.sleep(2)
        
        # Extrair dados da página atual
        extrair_dados_pagina()
    except Exception as e:
        print(f"Erro durante a navegação: {e}")
        break

# Fecha o navegador
driver.quit()

# Exporta os dados para um DataFrame e salva em CSV
df = pd.DataFrame(dados)
output_file = f"dados_renasem_{args.estado.lower()}.csv"
df.to_csv(output_file, index=False)

print(f"Dados extraídos e salvos em '{output_file}'")
