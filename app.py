import re
from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud


APP_DIR = Path(__file__).parent
DEFAULT_DATA = APP_DIR / "data" / "gagging_pop_news_sample.csv"
PUBLICATION_DATA_FILES = [
    APP_DIR / "data" / "billboard_ultimas_100_publicacoes.csv",
    APP_DIR / "data" / "pitchfork_ultimas_100_publicacoes.csv",
    APP_DIR / "data" / "rollingstone_ultimas_100_publicacoes.csv",
]

POSITIVE_WORDS_PT = {
    "amei",
    "amando",
    "bom",
    "boa",
    "excelente",
    "feliz",
    "hit",
    "iconico",
    "incrivel",
    "lindo",
    "melhor",
    "perfeito",
    "sucesso",
    "vencedora",
}

NEGATIVE_WORDS_PT = {
    "cancelado",
    "crise",
    "decepcionante",
    "fraco",
    "hate",
    "polemica",
    "problema",
    "ruim",
    "triste",
    "vazou",
}

STOPWORDS = {
    "a",
    "agora",
    "ao",
    "aos",
    "as",
    "com",
    "da",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "mais",
    "na",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "para",
    "por",
    "que",
    "sobre",
    "um",
    "uma",
    "x",
}

COLOR_SEQUENCE = ["#ef6f6c", "#2f9c95", "#f2b84b", "#5158bb", "#7a6f5a", "#d45b91"]

st.set_page_config(
    page_title="GAGGING | Pop Social Listening",
    page_icon="G",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --bg-soft: #fff0f7;
        --surface: #ffffff;
        --surface-alt: #ffe2f0;
        --ink: #1b1117;
        --muted: #6f4058;
        --accent: #ff2f92;
        --accent-2: #c6007e;
        --line: #f4bad7;
    }

    .stApp {
        background:
            linear-gradient(180deg, rgba(255, 224, 241, 0.98) 0%, rgba(255, 241, 248, 1) 45%, rgba(255, 232, 244, 1) 100%),
            var(--bg-soft);
        color: var(--ink);
    }

    section[data-testid="stSidebar"] {
        background: #ff2f92;
    }

    section[data-testid="stSidebar"] * {
        color: #111111 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="input"] > div,
    section[data-testid="stSidebar"] [data-baseweb="textarea"] > div,
    section[data-testid="stSidebar"] [data-testid="stDateInput"] input,
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background: #ffffff !important;
        border-color: #ffffff !important;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #ffe2f0 !important;
    }

    section[data-testid="stSidebar"] button {
        background: #ffffff !important;
        color: #111111 !important;
        border-color: #ffffff !important;
    }

    div[data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem 1rem 0.85rem;
        box-shadow: 0 10px 24px rgba(31, 41, 51, 0.07);
    }

    div[data-testid="stMetricLabel"] p {
        color: var(--muted);
        font-size: 0.9rem;
    }

    div[data-testid="stMetricValue"] {
        color: var(--ink);
    }

    .hero {
        padding: 1.35rem 0 0.6rem;
    }

    .hero-eyebrow {
        color: var(--accent-2);
        font-size: 0.86rem;
        font-weight: 700;
        letter-spacing: 0;
        text-transform: uppercase;
    }

    .hero h1 {
        color: var(--ink);
        font-size: clamp(2.25rem, 5vw, 4.4rem);
        line-height: 1;
        margin: 0.15rem 0 0.5rem;
    }

    .hero p {
        color: var(--muted);
        font-size: 1.05rem;
        max-width: 860px;
    }

    .source-note {
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 1.1rem;
    }

    div[data-testid="stTabs"] button p {
        font-weight: 650;
    }

    .stDataFrame {
        border: 1px solid var(--line);
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = COLOR_SEQUENCE


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^a-zà-ú0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def sentiment_score(text: str) -> float:
    cleaned = clean_text(text)
    words = set(cleaned.split())
    lexicon_score = len(words & POSITIVE_WORDS_PT) - len(words & NEGATIVE_WORDS_PT)
    blob_score = TextBlob(cleaned).sentiment.polarity
    return round(blob_score + (lexicon_score * 0.18), 3)


def sentiment_label(score: float) -> str:
    if score > 0.08:
        return "Positivo"
    if score < -0.08:
        return "Negativo"
    return "Neutro"


@st.cache_data
def load_default_data() -> pd.DataFrame:
    sample_data = pd.read_csv(DEFAULT_DATA, parse_dates=["data"])
    publication_data = [
        normalize_publication_data(path)
        for path in PUBLICATION_DATA_FILES
        if path.exists()
    ]
    if publication_data:
        return pd.concat([sample_data, *publication_data], ignore_index=True)
    return sample_data


def first_available_column(data: pd.DataFrame, columns: list[str], fallback: str = "") -> pd.Series:
    for column in columns:
        if column in data.columns:
            return data[column].fillna("")
    return pd.Series([fallback] * len(data), index=data.index)


def normalize_publication_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    published_at = first_available_column(data, ["data_publicacao", "data_sitemap", "data_publicacao_gmt"])
    topic = first_available_column(data, ["categorias", "secao", "tipo_conteudo"], "Publicacao")
    summary = first_available_column(data, ["resumo"])
    title = first_available_column(data, ["titulo"])
    author = first_available_column(data, ["autor"], "Sem autor")
    source = first_available_column(data, ["fonte"], path.stem.replace("_ultimas_100_publicacoes", "").title())
    link = first_available_column(data, ["link"])
    collected_at = first_available_column(data, ["data_coleta"], "coleta automatizada")

    normalized = pd.DataFrame(
        {
            "data": pd.to_datetime(published_at, errors="coerce"),
            "fonte": source,
            "artista": author.where(author.astype(str).str.strip() != "", "Sem autor"),
            "tema": topic.where(topic.astype(str).str.strip() != "", "Publicacao"),
            "texto": (title.astype(str).str.strip() + ". " + summary.astype(str).str.strip()).str.strip(),
            "curtidas": 1,
            "compartilhamentos": 0,
            "comentarios": 0,
            "url_origem": link,
            "coleta": collected_at,
        }
    )
    return normalized.dropna(subset=["data", "texto"])


def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    required_columns = [
        "data",
        "fonte",
        "artista",
        "tema",
        "texto",
        "curtidas",
        "compartilhamentos",
        "comentarios",
    ]
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        st.error(f"O arquivo enviado precisa conter estas colunas: {', '.join(missing)}")
        st.stop()

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df.dropna(subset=["data", "texto"])
    for column in ["curtidas", "compartilhamentos", "comentarios"]:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)

    df["texto_limpo"] = df["texto"].apply(clean_text)
    df["engajamento"] = df["curtidas"] + df["compartilhamentos"] + df["comentarios"]
    df["sentimento_score"] = df["texto_limpo"].apply(sentiment_score)
    df["sentimento"] = df["sentimento_score"].apply(sentiment_label)
    return df


def build_wordcloud(texts: pd.Series):
    joined = " ".join(texts.dropna().astype(str))
    tokens = [word for word in joined.split() if word not in STOPWORDS and len(word) > 2]
    if not tokens:
        return None
    return WordCloud(
        width=1200,
        height=520,
        background_color="white",
        colormap="Set2",
        max_words=100,
    ).generate(" ".join(tokens))


with st.sidebar:
    st.title("GAGGING")
    st.caption("Introdução à programação e visualização de dados")

    uploaded_file = st.file_uploader(
        "Carregar CSV",
        type=["csv"],
        help=(
            "Use as colunas: data, fonte, artista, tema, texto, curtidas, "
            "compartilhamentos, comentarios. Colunas extras, como url_origem, são aceitas."
        ),
    )

    if uploaded_file:
        raw_data = pd.read_csv(uploaded_file)
        data_origin = "CSV enviado"
    else:
        raw_data = load_default_data()
        data_origin = "Base com dados reais manualizados"

df = prepare_data(raw_data)

with st.sidebar:
    min_date = df["data"].min().date()
    max_date = df["data"].max().date()
    date_range = st.date_input("Período", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    selected_sources = st.multiselect("Fontes", sorted(df["fonte"].unique()), default=sorted(df["fonte"].unique()))
    selected_artists = st.multiselect("Artistas", sorted(df["artista"].unique()), default=sorted(df["artista"].unique()))
    selected_topics = st.multiselect("Temas", sorted(df["tema"].unique()), default=sorted(df["tema"].unique()))
    selected_sentiments = st.multiselect(
        "Sentimentos",
        ["Positivo", "Neutro", "Negativo"],
        default=["Positivo", "Neutro", "Negativo"],
    )

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["data"].dt.date >= start_date)
    & (df["data"].dt.date <= end_date)
    & (df["fonte"].isin(selected_sources))
    & (df["artista"].isin(selected_artists))
    & (df["tema"].isin(selected_topics))
    & (df["sentimento"].isin(selected_sentiments))
]

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Introdução à programação</div>
        <h1>GAGGING</h1>
        <p>Análise visual da repercussão de música pop a partir de registros do X,
        Billboard, Pitchfork e Rolling Stone organizados em CSV.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="source-note">{data_origin} | Dashboard interativo para observar engajamento, sentimentos e temas.</div>',
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("Nenhum registro encontrado com os filtros atuais.")
    st.stop()

total_posts = len(filtered)
total_engagement = int(filtered["engajamento"].sum())
top_artist = filtered.groupby("artista")["engajamento"].sum().idxmax()
dominant_sentiment = filtered["sentimento"].mode().iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Publicações analisadas", f"{total_posts:,}".replace(",", "."))
col2.metric("Engajamento total", f"{total_engagement:,}".replace(",", "."))
col3.metric("Artista em destaque", top_artist)
col4.metric("Sentimento dominante", dominant_sentiment)

tab_overview, tab_sentiment, tab_topics, tab_data = st.tabs(
    ["Visão geral", "Sentimentos", "Temas e palavras", "Dados e fontes"]
)

with tab_overview:
    chart_col1, chart_col2 = st.columns((1.25, 1))

    by_artist = (
        filtered.groupby("artista", as_index=False)["engajamento"]
        .sum()
        .sort_values("engajamento", ascending=False)
    )
    fig_artist = px.bar(
        by_artist,
        x="artista",
        y="engajamento",
        color="artista",
        title="Engajamento por artista",
        labels={"artista": "Artista", "engajamento": "Engajamento"},
    )
    fig_artist.update_layout(showlegend=False, title_font_size=18)

    by_source = filtered.groupby("fonte", as_index=False)["engajamento"].sum()
    fig_source = px.pie(
        by_source,
        names="fonte",
        values="engajamento",
        title="Participação das fontes no engajamento",
        hole=0.52,
    )
    fig_source.update_layout(title_font_size=18)

    chart_col1.plotly_chart(fig_artist, use_container_width=True)
    chart_col2.plotly_chart(fig_source, use_container_width=True)

    daily = filtered.groupby(filtered["data"].dt.date, as_index=False)["engajamento"].sum()
    daily.columns = ["data", "engajamento"]
    fig_daily = px.line(
        daily,
        x="data",
        y="engajamento",
        markers=True,
        title="Evolução do engajamento por data",
        labels={"data": "Data", "engajamento": "Engajamento"},
    )
    fig_daily.update_traces(line_width=3, marker_size=8)
    fig_daily.update_layout(title_font_size=18)
    st.plotly_chart(fig_daily, use_container_width=True)

with tab_sentiment:
    sent_col1, sent_col2 = st.columns((1, 1))

    sentiment_counts = filtered["sentimento"].value_counts().reset_index()
    sentiment_counts.columns = ["sentimento", "quantidade"]
    fig_sentiment = px.bar(
        sentiment_counts,
        x="sentimento",
        y="quantidade",
        color="sentimento",
        title="Distribuição de sentimentos",
        category_orders={"sentimento": ["Positivo", "Neutro", "Negativo"]},
    )

    sentiment_artist = (
        filtered.groupby(["artista", "sentimento"], as_index=False)
        .size()
        .rename(columns={"size": "quantidade"})
    )
    fig_sentiment_artist = px.bar(
        sentiment_artist,
        x="artista",
        y="quantidade",
        color="sentimento",
        barmode="group",
        title="Sentimentos por artista",
    )

    sent_col1.plotly_chart(fig_sentiment, use_container_width=True)
    sent_col2.plotly_chart(fig_sentiment_artist, use_container_width=True)

    st.dataframe(
        filtered[["data", "fonte", "artista", "tema", "sentimento", "sentimento_score", "texto"]]
        .sort_values("data", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

with tab_topics:
    topic_col1, topic_col2 = st.columns((1, 1))

    by_topic = (
        filtered.groupby("tema", as_index=False)
        .agg(publicacoes=("texto", "count"), engajamento=("engajamento", "sum"))
        .sort_values("engajamento", ascending=False)
    )
    fig_topic = px.scatter(
        by_topic,
        x="publicacoes",
        y="engajamento",
        size="engajamento",
        color="tema",
        title="Temas: volume de publicações x engajamento",
        labels={"publicacoes": "Publicações", "engajamento": "Engajamento"},
    )
    topic_col1.plotly_chart(fig_topic, use_container_width=True)

    all_words = " ".join(filtered["texto_limpo"]).split()
    word_counts = Counter(word for word in all_words if word not in STOPWORDS and len(word) > 2)
    top_words = pd.DataFrame(word_counts.most_common(12), columns=["palavra", "frequencia"])
    fig_words = px.bar(
        top_words,
        x="frequencia",
        y="palavra",
        orientation="h",
        title="Palavras mais frequentes",
    )
    fig_words.update_layout(yaxis={"categoryorder": "total ascending"})
    topic_col2.plotly_chart(fig_words, use_container_width=True)

    wordcloud = build_wordcloud(filtered["texto_limpo"])
    if wordcloud:
        st.image(wordcloud.to_array(), caption="Nuvem de palavras das publicações filtradas")

    st.subheader("Ranking de assuntos")
    st.dataframe(by_topic, use_container_width=True, hide_index=True)

with tab_data:
    st.write("A tabela reúne os dados tratados, incluindo engajamento, sentimento e URLs de referência quando disponíveis.")
    preferred_columns = [
        "data",
        "fonte",
        "artista",
        "tema",
        "texto",
        "curtidas",
        "compartilhamentos",
        "comentarios",
        "engajamento",
        "sentimento",
        "url_origem",
        "coleta",
    ]
    visible_columns = [column for column in preferred_columns if column in filtered.columns]
    st.dataframe(
        filtered.sort_values("engajamento", ascending=False)[visible_columns],
        use_container_width=True,
        hide_index=True,
    )

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Baixar dados filtrados",
        data=csv,
        file_name="gagging_dados_filtrados.csv",
        mime="text/csv",
    )

st.caption("Desenvolvido para a disciplina Introdução à Programação da FGV Comunicação.")
