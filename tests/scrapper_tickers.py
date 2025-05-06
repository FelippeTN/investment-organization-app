import requests
from bs4 import BeautifulSoup

def obter_tickers_fundamentus():
    url = "https://www.fundamentus.com.br/resultado.php"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.post(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    tabela = soup.find('table', {'id': 'resultado'})
    tickers = []

    if tabela:
        linhas = tabela.find_all('tr')[1:]  # pula o cabeçalho
        for linha in linhas:
            colunas = linha.find_all('td')
            if colunas:
                ticker = colunas[0].text.strip()
                tickers.append(ticker)

    return tickers

# Executar
tickers = obter_tickers_fundamentus()
print(f"Total de tickers encontrados: {len(tickers)}")
print(tickers[:10])  
