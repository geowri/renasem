# RENASEM Data Downloader

Este repositório fornece um script para baixar dados diretamente do portal RENASEM (Registro Nacional de Sementes e Mudas) e processá-los utilizando a base de dados de CNPJ da receita federal. Utilizamos Selenium para automação de navegador, além de bibliotecas adicionais para manipulação de dados.

## Requisitos

1. **Chromium e Chromium-Driver**  

```bash
sudo apt install chromium-browser chromium-driver
```

2. **Criar Ambiente Virtual**

```bash
python3 -m venv venv
```
2. **Ativar o Ambiente Virtual no terminal**

```bash
source venv/bin/activate
```

3. **Ativar o Anaconda no terminal**  
```bash
pip install selenium pandas requests
```

4. **Iniciar Script**
Baixa todos os dados
```bash
python get_data_renascem.py
```
Baixa por estado passando o argumento com a sigla do estado desejado
```bash
python get_data_renascem_by_state.py PA
```
