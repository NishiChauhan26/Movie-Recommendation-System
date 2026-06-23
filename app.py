import streamlit as st
import pickle
import requests

# PAGE CONFIG
st.set_page_config(
    page_title="CineMatch — Movie Recommendations",
    page_icon="🎬",
    layout="wide"
)

# LOAD DATA
movies = pickle.load(open('movie_list.pkl', 'rb'))
vectors = pickle.load(open('vectors.pkl', 'rb'))

# TMDB API KEY
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# LOAD SIMILARITY
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

# FETCH POSTER
PLACEHOLDER = "https://placehold.co/300x450/1c1f2e/8892b0?text=No+Poster"

def fetch_poster(movie_id):
    for attempt in range(3):
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue
            data = response.json()
            poster_path = data.get('poster_path')
            if not poster_path:
                return PLACEHOLDER
            return "https://image.tmdb.org/t/p/w500" + poster_path
        except Exception as e:
            print(f"Attempt {attempt+1} failed for movie_id {movie_id}: {e}")
    return PLACEHOLDER

# RECOMMEND FUNCTION
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = int(movies.iloc[i[0]].movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

# ─ CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #0a0c14;
    font-family: 'Inter', sans-serif;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── HERO BANNER ── */
.hero {
    background: linear-gradient(
        135deg,
        #0a0c14 0%,
        #0d1117 40%,
        #12071a 100%
    );
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    padding: 52px 64px 44px;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 20%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(236,72,153,0.07) 0%, transparent 70%);
    pointer-events: none;
}

.hero-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #8b5cf6;
    margin-bottom: 10px;
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 72px;
    line-height: 1;
    letter-spacing: 2px;
    background: linear-gradient(135deg, #ffffff 30%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 12px;
}

.hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: #64748b;
    letter-spacing: 0.3px;
}

/* ── SEARCH SECTION ── */
.search-section {
    background: #0d0f1a;
    padding: 36px 64px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.search-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 12px;
}

/* Selectbox styling */
div[data-testid="stSelectbox"] > div > div {
    background: #131622 !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 4px 8px !important;
    transition: border-color 0.2s ease !important;
}

div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 4px !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #9333ea) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(139,92,246,0.35) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── RESULTS SECTION ── */
.results-section {
    padding: 44px 64px 60px;
}

.results-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 32px;
}

.results-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 6px;
}

.results-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 32px;
    letter-spacing: 1.5px;
    color: #f1f5f9;
    margin: 0;
}

.results-divider {
    width: 3px;
    height: 36px;
    background: linear-gradient(180deg, #8b5cf6, #ec4899);
    border-radius: 2px;
}

/* ── MOVIE CARD ── */
.movie-card-wrap {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    cursor: pointer;
    background: #131622;
}

.movie-card-wrap:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 20px 48px rgba(0,0,0,0.6), 0 0 0 1px rgba(139,92,246,0.3);
}

.movie-card-wrap img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    border-radius: 12px;
}

.movie-rank {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0,0,0,0.75);
    backdrop-filter: blur(6px);
    color: #a78bfa;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 3px 8px;
    border-radius: 5px;
    border: 1px solid rgba(139,92,246,0.3);
}

.movie-title-card {
    font-family: 'Inter', sans-serif;
    text-align: center;
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 500;
    margin-top: 10px;
    line-height: 1.4;
    padding: 0 4px;
    letter-spacing: 0.2px;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #8b5cf6 !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 80px 40px;
    color: #334155;
}
.empty-icon {
    font-size: 56px;
    margin-bottom: 16px;
}
.empty-text {
    font-size: 18px;
    font-weight: 500;
    color: #475569;
}
.empty-sub {
    font-size: 14px;
    color: #334155;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI-Powered Discovery</div>
    <div class="hero-title">CineMatch</div>
    <div class="hero-sub">Content-based recommendations from a library of thousands of films</div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = movies['title'].values[0]
if "show_recommendations" not in st.session_state:
    st.session_state.show_recommendations = False

# ── SEARCH ────────────────────────────────────────────────────────────────────
st.markdown('<div class="search-section">', unsafe_allow_html=True)
st.markdown('<div class="search-label">Pick a movie you love</div>', unsafe_allow_html=True)

col_search, col_gap, col_btn = st.columns([5, 0.3, 1.5])

with col_search:
    selected_movie = st.selectbox(
        label="",
        options=movies['title'].values,
        index=list(movies['title'].values).index(st.session_state.selected_movie),
        key="movie_selectbox",
        label_visibility="collapsed"
    )
    st.session_state.selected_movie = selected_movie

with col_btn:
    recommend_clicked = st.button("✦ Find Similar Movies")

st.markdown('</div>', unsafe_allow_html=True)

if recommend_clicked:
    st.session_state.show_recommendations = True

# ── RESULTS ───────────────────────────────────────────────────────────────────
if st.session_state.show_recommendations:
    with st.spinner("Analysing film DNA..."):
        names, posters = recommend(st.session_state.selected_movie)

    st.markdown("""
    <div class="results-section">
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:32px;">
            <div style="width:3px; height:36px; background:linear-gradient(180deg,#8b5cf6,#ec4899); border-radius:2px;"></div>
            <div>
                <div class="results-label">Because you picked</div>
                <div class="results-title">Recommended for you</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pad outer columns to match search section indent
    _, inner, _ = st.columns([0.05, 11, 0.05])
    with inner:
        cols = st.columns(5, gap="large")
        ranks = ["#1 Pick", "#2", "#3", "#4", "#5"]

        for i in range(5):
            with cols[i]:
                poster_url = posters[i] if posters[i] else PLACEHOLDER

                # Card HTML with rank badge
                st.markdown(f"""
                <div class="movie-card-wrap">
                    <div class="movie-rank">{ranks[i]}</div>
                    <img src="{poster_url}" alt="{names[i]}" onerror="this.src='{PLACEHOLDER}'"/>
                </div>
                <div class="movie-title-card">{names[i]}</div>
                """, unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎬</div>
        <div class="empty-text">Your recommendations will appear here</div>
        <div class="empty-sub">Search for a movie above and click "Find Similar Movies"</div>
    </div>
    """, unsafe_allow_html=True)