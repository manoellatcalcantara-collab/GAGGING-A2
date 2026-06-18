# GAGGING

Dashboard em Streamlit para analisar a repercussao de noticias e conversas sobre musica pop em redes sociais e portais jornalisticos.

O projeto foi adaptado para a disciplina de **Introducao a programacao**. Ele combina tratamento de texto, metricas de engajamento, analise de sentimento e graficos interativos.

## Funcionalidades

- Base CSV com registros reais/manualizados do X, Billboard, Pitchfork e Rolling Stone.
- Inclusao dos arquivos brutos `billboard_ultimas_100_publicacoes.csv`, `pitchfork_ultimas_100_publicacoes.csv` e `rollingstone_ultimas_100_publicacoes.csv` em `data/`.
- Carregamento automatico das publicacoes recentes desses tres veiculos na base padrao do dashboard.
- Upload de CSV proprio.
- Filtros por periodo, fonte, artista/autor, tema e sentimento.
- Indicadores de publicacoes, engajamento total, artista/autor em destaque e sentimento dominante.
- Graficos interativos com Plotly.
- Analise de sentimento simples com TextBlob e lexico complementar em portugues.
- Nuvem de palavras e ranking de temas.
- Download dos dados filtrados.

## Estrutura do projeto

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
|-- data/
|   |-- gagging_pop_news_sample.csv
|   |-- billboard_ultimas_100_publicacoes.csv
|   |-- pitchfork_ultimas_100_publicacoes.csv
|   |-- rollingstone_ultimas_100_publicacoes.csv
|   |-- fontes_reais.md
|-- coleta_colab_opcional.md
```

## Fontes dos dados

Os dados do dashboard combinam uma base amostral tratada com os CSVs recentes de Billboard, Pitchfork e Rolling Stone. Os tres arquivos brutos ficam preservados em `data/` para consulta, auditoria e novas transformacoes.

## Observacao sobre o X

Os registros do X foram organizados por manualizacao de posts publicos e perfis oficiais, pois a coleta automatica completa do X normalmente exige credenciais de API e respeito aos termos de uso da plataforma.
