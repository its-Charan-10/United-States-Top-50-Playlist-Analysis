"""
7_Executive_Summary.py
----------------------
Executive Summary page for the United States Top 50 Playlist
Performance and Song Popularity Trend Analysis project.

Sections
--------
1. Auto-generated Insights (Colorful Metric Cards)
2. Album vs Single Comparison
3. Top 5 Recommendations for Atlantic Recording Corporation
"""

import sys
import os

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.loader import load_data
from utils.preprocessing import preprocess_data
from utils.feature_engineering import feature_engineering

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Shared CSS & Custom Cards
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] { background-color: #0e1117; }

        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            color: #e2e8f0;
            margin: 35px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #2d3561;
        }

        /* Colorful Insight Cards */
        .insight-card {
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .insight-card-title {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            opacity: 0.85;
            margin-bottom: 8px;
        }
        .insight-card-value {
            font-size: 1.6rem;
            font-weight: 700;
            line-height: 1.2;
        }

        /* Gradients for cards */
        .bg-purple  { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .bg-blue    { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .bg-green   { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: #0d1117 !important;}
        .bg-orange  { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: #0d1117 !important;}
        .bg-red     { background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%); }
        .bg-dark    { background: linear-gradient(135deg, #1a1d27 0%, #16213e 100%); border: 1px solid #2d3561; }

        .recommendation-box {
            background-color: #1a1d27;
            border-left: 5px solid #4facfe;
            padding: 16px 20px;
            margin-bottom: 16px;
            border-radius: 4px;
            font-size: 1rem;
            color: #e2e8f0;
        }
        .recommendation-title {
            font-weight: 700;
            color: #4facfe;
            margin-bottom: 4px;
            font-size: 1.1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data pipeline
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner="🔄 Loading and preparing data…")
def load_pipeline() -> pd.DataFrame:
    raw = load_data()
    clean = preprocess_data(raw)
    enriched = feature_engineering(clean)
    return enriched


# ---------------------------------------------------------------------------
# UI Helpers
# ---------------------------------------------------------------------------


def insight_card(title: str, value: str, color_class: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card {color_class}">
            <div class="insight-card-title">{title}</div>
            <div class="insight-card-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Core Analysis & Rendering
# ---------------------------------------------------------------------------


def render_insights(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">🔍 Key Discoveries & Insights</p>', unsafe_allow_html=True)

    # 1. Most Dominant Artist
    most_dominant = "N/A"
    if "artist_dominance_index" in df.columns and "artist" in df.columns and not df.empty:
        top_a = df.drop_duplicates("artist").nlargest(1, "artist_dominance_index")
        if not top_a.empty:
            most_dominant = f"{top_a.iloc[0]['artist']} <span style='font-size:1rem; opacity:0.8;'>({int(top_a.iloc[0]['artist_dominance_index'])} idx)</span>"

    # 2. Longest Charting Song
    longest_song = "N/A"
    if "days_on_chart" in df.columns and "song" in df.columns and not df.empty:
        top_l = df.drop_duplicates("song").nlargest(1, "days_on_chart")
        if not top_l.empty:
            longest_song = f"{top_l.iloc[0]['song']} <span style='font-size:1rem; opacity:0.8;'>({int(top_l.iloc[0]['days_on_chart'])} days)</span>"

    # 3. Most Stable Song
    stable_song = "N/A"
    if "rank_volatility" in df.columns and "song" in df.columns and not df.empty:
        top_s = df.drop_duplicates("song").dropna(subset=["rank_volatility"]).nsmallest(1, "rank_volatility")
        if not top_s.empty:
            stable_song = f"{top_s.iloc[0]['song']} <span style='font-size:1rem; opacity:0.8;'>(±{top_s.iloc[0]['rank_volatility']:.2f})</span>"

    # 4. Highest Popularity Song
    highest_pop = "N/A"
    if "popularity" in df.columns and "song" in df.columns and not df.empty:
        top_p = df.drop_duplicates("song").nlargest(1, "popularity")
        if not top_p.empty:
            highest_pop = f"{top_p.iloc[0]['song']} <span style='font-size:1rem; opacity:0.8;'>({int(top_p.iloc[0]['popularity'])}/100)</span>"

    # 5. Average Popularity
    avg_pop = "N/A"
    if "popularity" in df.columns and not df.empty:
        avg_pop = f"{df['popularity'].mean():.1f} / 100"

    # 6. Explicit Content Percentage
    explicit_pct = "N/A"
    if "is_explicit" in df.columns and not df.empty:
        explicit_pct = f"{df['is_explicit'].mean() * 100:.1f}%"

    # 7. Average Rank
    avg_rank = "N/A"
    if "position" in df.columns and not df.empty:
        avg_rank = f"#{df['position'].mean():.1f}"

    # Row 1
    c1, c2, c3, c4 = st.columns(4)
    with c1: insight_card("👑 Most Dominant Artist", most_dominant, "bg-purple")
    with c2: insight_card("⏳ Longest Charting Song", longest_song, "bg-blue")
    with c3: insight_card("⚓ Most Stable Rank", stable_song, "bg-green")
    with c4: insight_card("🔥 Highest Popularity", highest_pop, "bg-red")

    # Row 2
    c5, c6, c7, c8 = st.columns(4)
    with c5: insight_card("⭐ Average Popularity", avg_pop, "bg-dark")
    with c6: insight_card("📈 Average Playlist Rank", avg_rank, "bg-dark")
    with c7: insight_card("🔞 Explicit Content", explicit_pct, "bg-dark")
    
    # 8. Album vs Single Comparison
    with c8:
        if "album_type" in df.columns and not df.empty:
            album_cnt = len(df[df["album_type"].str.lower() == "album"]["song"].unique())
            single_cnt = len(df[df["album_type"].str.lower() == "single"]["song"].unique())
            insight_card("💿 Album vs Single", f"{album_cnt} Albums | {single_cnt} Singles", "bg-orange")
        else:
            insight_card("💿 Album vs Single", "N/A", "bg-orange")


def render_recommendations() -> None:
    st.markdown('<p class="section-header">🎯 Top 5 Recommendations for Atlantic Recording Corporation</p>', unsafe_allow_html=True)
    
    recs = [
        {
            "title": "1. Capitalize on Artist Dominance and Cross-Promotion",
            "desc": "The data shows that a small cluster of artists consistently commands the highest dominance index. Focus marketing spend and collaboration efforts on these established pillars to anchor new releases, leveraging their vast charting longevity to introduce emerging artists through features."
        },
        {
            "title": "2. Optimize Track Duration for Algorithmic Success",
            "desc": "Average track durations and correlation metrics indicate a sweet spot for stream retention. Avoid excessively long tracks (over 4 minutes) for lead singles targeting the Top 50, prioritizing immediate engagement and higher replay value."
        },
        {
            "title": "3. Leverage the Single vs. Album Release Strategy",
            "desc": "While albums generate bulk catalogue streams, individual singles often exhibit lower rank volatility and higher peak popularity. Stagger major album rollouts with consistent, high-quality single releases to maintain a continuous presence in the Top 50 ecosystem."
        },
        {
            "title": "4. Explicit Content Strategy and Audience Targeting",
            "desc": "A significant percentage of the Top 50 relies on explicit tracks, which often correlate with highly engaged demographics. Ensure explicit releases are heavily promoted on platforms that index well with younger audiences, while producing clean edits strictly for terrestrial radio compliance."
        },
        {
            "title": "5. Monitor Rank Volatility for Playlist Placements",
            "desc": "Songs with 'stable' or 'slowly declining' movements are the backbone of passive listening. Pitch these tracks to broader, mood-based playlists to extend their lifecycle, while reserving aggressive marketing pushes for 'fastest-rising' tracks showing viral potential."
        }
    ]

    for rec in recs:
        st.markdown(
            f"""
            <div class="recommendation-box">
                <div class="recommendation-title">{rec['title']}</div>
                {rec['desc']}
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------


def render_footer() -> None:
    st.markdown(
        '<div class="dashboard-footer" style="margin-top: 60px;">'
        "Developed using <strong>Streamlit</strong> + <strong>Plotly</strong> + <strong>Pandas</strong>"
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    st.title("📋 Executive Summary")
    st.markdown(
        "A high-level strategic overview of the **United States Top 50 Playlist**, "
        "distilling complex charting data into actionable insights for label executives."
    )
    
    try:
        df_full = load_pipeline()
    except Exception as exc:
        st.error(f"**Error loading data.** {exc}")
        st.stop()

    if df_full.empty:
        st.warning("⚠️ No data available to generate the executive summary.")
        return

    # Use the full dataset (no sidebar filters needed for an executive summary, 
    # but we can omit the sidebar entirely to keep it clean and executive-focused)
    st.sidebar.markdown("## 📋 Executive Summary")
    st.sidebar.info(
        "This page provides a static, top-level analysis of the complete dataset "
        "to deliver immediate strategic value."
    )

    render_insights(df_full)
    render_recommendations()
    render_footer()


if __name__ == "__main__" or True:
    main()
