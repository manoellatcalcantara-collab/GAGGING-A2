# Fontes e criterios da base CSV

A base `gagging_pop_news_sample.csv` foi refeita para usar registros rastreaveis do X, Billboard, Pitchfork e Rolling Stone.

Alem da base amostral tratada, o repositorio inclui estes arquivos brutos em `data/`:

- `billboard_ultimas_100_publicacoes.csv`
- `pitchfork_ultimas_100_publicacoes.csv`
- `rollingstone_ultimas_100_publicacoes.csv`

O app normaliza automaticamente esses tres CSVs para o formato usado no dashboard.

## Criterio de organizacao

- `fonte`: plataforma ou veiculo usado como referencia.
- `texto`: titulo e resumo da publicacao, ou resumo curto/manualizado para analise no dashboard.
- `artista`: no caso dos CSVs jornalisticos recentes, recebe o autor da publicacao para manter compatibilidade com os filtros existentes.
- `tema`: categoria, secao ou tipo de conteudo do registro.
- `curtidas`, `compartilhamentos` e `comentarios`: valores organizados para fins de visualizacao e comparacao no projeto. Nos CSVs jornalisticos recentes, cada publicacao entra com `curtidas = 1` para aparecer nos graficos de volume.
- `url_origem`: pagina publica de referencia.
- `coleta`: tipo ou data de coleta usada no registro.

## Observacao sobre X

O X limita coleta automatizada completa sem credenciais de API. Por isso, as linhas do X foram manualizadas a partir de perfis publicos, mantendo URL de perfil como referencia.

## Paginas de referencia

- X: https://x.com/SabrinaAnnLynn
- X: https://x.com/taylorswift13
- X: https://x.com/billboard
- Billboard: https://www.billboard.com/music/
- Billboard Hot 100: https://www.billboard.com/charts/hot-100/
- Pitchfork: https://pitchfork.com/
- Rolling Stone Music News: https://www.rollingstone.com/music/music-news/
- Rolling Stone Reviews: https://www.rollingstone.com/music/music-album-reviews/
