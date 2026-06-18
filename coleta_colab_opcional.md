# Coleta opcional com Google Colab

Use este roteiro se quiser coletar, conferir ou ampliar dados reais antes de enviar para o dashboard.

## Quando usar Colab

O Colab é útil quando o computador não tem Python instalado ou quando você quer gerar o CSV em um notebook compartilhável.

## Modelo de notebook

Crie um notebook no Google Colab e rode:

```python
!pip install pandas requests beautifulsoup4
```

```python
import pandas as pd

dados = [
    {
        "data": "2025-06-16",
        "fonte": "Billboard",
        "artista": "Sabrina Carpenter",
        "tema": "Charts",
        "texto": "Billboard reportou que Manchild estreou em primeiro lugar na Hot 100.",
        "curtidas": 12800,
        "compartilhamentos": 2600,
        "comentarios": 1400,
        "url_origem": "https://www.billboard.com/charts/hot-100/",
        "coleta": "checagem editorial",
    }
]

df = pd.DataFrame(dados)
df.to_csv("gagging_dados_reais.csv", index=False)
df
```

Depois, baixe o arquivo `gagging_dados_reais.csv` e carregue no dashboard pela sidebar.

## Exemplo simples com BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.billboard.com/"
headers = {"User-Agent": "Mozilla/5.0"}
html = requests.get(url, headers=headers, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

titulos = [item.get_text(strip=True) for item in soup.find_all(["h2", "h3"])[:10]]
titulos
```

Transforme as notícias encontradas no formato exigido pelo dashboard:

```python
linhas = []
for titulo in titulos:
    linhas.append({
        "data": "2026-06-18",
        "fonte": "Billboard",
        "artista": "Não identificado",
        "tema": "Notícia",
        "texto": titulo,
        "curtidas": 0,
        "compartilhamentos": 0,
        "comentarios": 0,
        "url_origem": url,
        "coleta": "rascunho automatizado",
    })

pd.DataFrame(linhas).to_csv("gagging_portais.csv", index=False)
```

## Sobre dados do X/Twitter

Para coletar do X com Tweepy, você precisa de credenciais oficiais da API. Sem isso, a alternativa recomendada para apresentação acadêmica é usar dados exportados/manualizados em CSV, sempre respeitando termos de uso, contexto e privacidade.
