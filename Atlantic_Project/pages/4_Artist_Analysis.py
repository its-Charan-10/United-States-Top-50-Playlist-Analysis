"""
4_Artist_Analysis.py
--------------------
Artist Performance Analysis page for the United States Top 50 Playlist
Performance and Song Popularity Trend Analysis project.

Sections
--------
1. Sidebar filters (Artist, Date, Album Type)
2. KPI Cards (5 metrics)
3. Chart Gallery (8 visualisations including Treemap & Bubble Chart)
4. Top Artists table
5. Top Songs Per Artist table
"""

import sys
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.loader import load_data
from utils.preprocessing import preprocess_data
from utils.feature_engineering import feature_engineering
from utils import charts

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Artist Performance Analysis",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Shared CSS
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] { background-color: #0e1117; }

        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1a1d27 0%, #16213e 100%);
            border: 1px solid #2d3561;
            border-radius: 12px;
            padding: 18px 22px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        div[data-testid="metric-container"] label {
            color: #a0aec0 !important;
            font-size: 0.80rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em !important;
        }
        div[data-testid="metric-container"] [data-testid="metric-value"] {
            color: #e2e8f0 !important;
            font-size: 1.65rem !important;
            font-weight: 700 !important;
        }
        .section-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #e2e8f0;
            margin: 28px 0 10px 0;
            padding-bottom: 6px;
            border-bottom: 2px solid #2d3561;
        }
        [data-testid="stSidebar"] {
            background-color: #0d1117;
            border-right: 1px solid #1e2432;
        }
        .dashboard-footer {
            text-align: center;
            color: #4a5568;
            font-size: 0.78rem;
            padding: 28px 0 12px 0;
            border-top: 1px solid #1e2432;
            margin-top: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

_TEMPLATE = "plotly_dark"

# ---------------------------------------------------------------------------
# Data pipeline — cached
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner="🔄 Loading and preparing data…")
def load_pipeline() -> pd.DataFrame:
    raw = load_data()
    clean = preprocess_data(raw)
    enriched = feature_engineering(clean)
    return enriched


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.markdown("## 🎤 Artist Filters")
        st.divider()

        all_artists = sorted(df["artist"].dropna().unique().tolist())
        selected_artists = st.multiselect(
            "🎤 Artist", options=all_artists,
            default=[], placeholder="All artists",
        )

        date_min = df["date"].min()
        date_max = df["date"].max()
        selected_dates = st.date_input(
            "📅 Date Range",
            value=(date_min.date(), date_max.date()),
            min_value=date_min.date(),
            max_value=date_max.date(),
        )
        if isinstance(selected_dates, (list, tuple)) and len(selected_dates) == 2:
            start_date = pd.Timestamp(selected_dates[0])
            end_date   = pd.Timestamp(selected_dates[1])
        else:
            start_date = end_date = pd.Timestamp(selected_dates[0])

        if "album_type" in df.columns:
            all_album_types = sorted(df["album_type"].dropna().unique().tolist())
            selected_album_types = st.multiselect(
                "💿 Album Type", options=all_album_types,
                default=[], placeholder="All album types",
            )
        else:
            selected_album_types = []

    filtered = df.copy()
    if selected_artists:
        filtered = filtered[filtered["artist"].isin(selected_artists)]
    filtered = filtered[
        (filtered["date"] >= start_date) & (filtered["date"] <= end_date)
    ]
    if selected_album_types and "album_type" in filtered.columns:
        filtered = filtered[filtered["album_type"].isin(selected_album_types)]

    return filtered.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Section 1 — KPI Cards
# ---------------------------------------------------------------------------


def render_kpis(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">📌 Artist KPIs</p>', unsafe_allow_html=True)

    agg = df.drop_duplicates("artist") if "artist" in df.columns else pd.DataFrame()

    total_artists = len(agg)

    most_dominant = "N/A"
    if "artist_dominance_index" in agg.columns and not agg.empty:
        top_d = agg.nlargest(1, "artist_dominance_index")
        if not top_d.empty:
            most_dominant = f"{top_d.iloc[0]['artist']}"

    highest_avg_pop = "N/A"
    if "artist_average_popularity" in agg.columns and not agg.empty:
        top_p = agg.nlargest(1, "artist_average_popularity")
        if not top_p.empty:
            highest_avg_pop = f"{top_p.iloc[0]['artist']} ({top_p.iloc[0]['artist_average_popularity']:.1f})"

    highest_chart_days = "N/A"
    if "artist_total_chart_days" in agg.columns and not agg.empty:
        top_c = agg.nlargest(1, "artist_total_chart_days")
        if not top_c.empty:
            highest_chart_days = f"{top_c.iloc[0]['artist']} ({int(top_c.iloc[0]['artist_total_chart_days'])} days)"

    avg_songs = (
        round(agg["artist_song_count"].mean(), 1)
        if "artist_song_count" in agg.columns and not agg.empty else "N/A"
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🎤 Total Artists", total_artists)
    c2.metric("👑 Most Dominant", most_dominant)
    c3.metric("🔥 Highest Avg Pop", highest_avg_pop)
    c4.metric("📅 Most Chart Days", highest_chart_days)
    c5.metric("🎵 Avg Songs/Artist", avg_songs)


# ---------------------------------------------------------------------------
# Inline chart helpers
# ---------------------------------------------------------------------------


def _artist_popularity_comparison(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    if "artist_average_popularity" not in df.columns or "artist" not in df.columns:
        return go.Figure()
    
    top = df.drop_duplicates("artist").nlargest(top_n, "artist_average_popularity")
    fig = px.bar(
        top.sort_values("artist_average_popularity", ascending=True),
        x="artist_average_popularity", y="artist",
        orientation="h",
        title=f"Top {top_n} Artists by Average Popularity",
        labels={"artist_average_popularity": "Avg Popularity", "artist": "Artist"},
        color="artist_average_popularity",
        color_continuous_scale="magma",
        template=_TEMPLATE,
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig


def _artist_song_count(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    if "artist_song_count" not in df.columns or "artist" not in df.columns:
        return go.Figure()

    top = df.drop_duplicates("artist").nlargest(top_n, "artist_song_count")
    fig = px.bar(
        top.sort_values("artist_song_count", ascending=True),
        x="artist_song_count", y="artist",
        orientation="h",
        title=f"Top {top_n} Artists by Song Count",
        labels={"artist_song_count": "Total Songs", "artist": "Artist"},
        color="artist_song_count",
        color_continuous_scale="teal",
        template=_TEMPLATE,
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig


def _artist_timeline(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    if "artist_dominance_index" not in df.columns:
        return go.Figure()
    
    top_artists = df.drop_duplicates("artist").nlargest(top_n, "artist_dominance_index")["artist"]
    subset = df[df["artist"].isin(top_artists)]
    
    fig = px.scatter(
        subset,
        x="date", y="artist",
        color="artist",
        title=f"Artist Timeline — Top {top_n} Dominant Artists",
        labels={"date": "Date", "artist": "Artist"},
        opacity=0.6,
        template=_TEMPLATE,
    )
    fig.update_traces(marker=dict(size=6))
    fig.update_layout(showlegend=False)
    return fig


def _artist_treemap(df: pd.DataFrame, top_n: int = 50) -> go.Figure:
    if "artist_dominance_index" not in df.columns:
        return go.Figure()
    
    top = df.drop_duplicates("artist").nlargest(top_n, "artist_dominance_index")
    top["Label"] = "Artists"
    
    fig = px.treemap(
        top,
        path=["Label", "artist"],
        values="artist_dominance_index",
        color="artist_dominance_index",
        color_continuous_scale="Blues",
        title=f"Artist Dominance Treemap (Top {top_n})",
        template=_TEMPLATE,
    )
    return fig


def _artist_bubble_chart(df: pd.DataFrame, top_n: int = 30) -> go.Figure:
    if "artist_song_count" not in df.columns or "artist_total_chart_days" not in df.columns:
        return go.Figure()
        
    top = df.drop_duplicates("artist").nlargest(top_n, "artist_dominance_index")
    
    fig = px.scatter(
        top,
        x="artist_total_chart_days", y="artist_average_popularity",
        size="artist_song_count", color="artist",
        hover_name="artist",
        title=f"Artist Bubble Chart (Top {top_n})",
        labels={
            "artist_total_chart_days": "Chart Days",
            "artist_average_popularity": "Avg Popularity",
            "artist_song_count": "Songs"
        },
        template=_TEMPLATE,
        size_max=40,
    )
    fig.update_layout(showlegend=False)
    return fig


# ---------------------------------------------------------------------------
# Section 2 — Chart Gallery
# ---------------------------------------------------------------------------


def render_charts(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">📊 Visualisations</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        try:
            st.plotly_chart(charts.top_artists_chart(df, top_n=15), use_container_width=True)
        except Exception as e:
            st.warning(f"Top Artists Chart: {e}")
    with c2:
        try:
            st.plotly_chart(charts.artist_dominance_chart(df, top_n=15), use_container_width=True)
        except Exception as e:
            st.warning(f"Artist Dominance Chart: {e}")

    c3, c4 = st.columns(2)
    with c3:
        try:
            st.plotly_chart(_artist_popularity_comparison(df, top_n=15), use_container_width=True)
        except Exception as e:
            st.warning(f"Artist Popularity Comparison: {e}")
    with c4:
        try:
            st.plotly_chart(_artist_song_count(df, top_n=15), use_container_width=True)
        except Exception as e:
            st.warning(f"Artist Song Count: {e}")

    try:
        st.plotly_chart(_artist_timeline(df, top_n=15), use_container_width=True)
    except Exception as e:
        st.warning(f"Artist Timeline: {e}")

    c5, c6 = st.columns(2)
    with c5:
        try:
            st.plotly_chart(_artist_treemap(df, top_n=30), use_container_width=True)
        except Exception as e:
            st.warning(f"Artist Treemap: {e}")
    with c6:
        try:
            st.plotly_chart(_artist_bubble_chart(df, top_n=30), use_container_width=True)
        except Exception as e:
            st.warning(f"Artist Bubble Chart: {e}")


# ---------------------------------------------------------------------------
# Section 3 & 4 — Tables
# ---------------------------------------------------------------------------


def render_tables(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">🏆 Top Artists Overview</p>', unsafe_allow_html=True)
    
    req = {
        "artist", "artist_song_count", "artist_total_chart_days",
        "artist_average_popularity", "artist_dominance_index"
    }
    if req.issubset(df.columns):
        t1 = (
            df[list(req)]
            .drop_duplicates("artist")
            .sort_values("artist_dominance_index", ascending=False)
            .head(30)
            .reset_index(drop=True)
        )
        t1.index += 1
        t1["artist_average_popularity"] = t1["artist_average_popularity"].round(1)
        t1 = t1.rename(columns={
            "artist": "Artist",
            "artist_song_count": "Songs",
            "artist_total_chart_days": "Chart Days",
            "artist_average_popularity": "Average Popularity",
            "artist_dominance_index": "Dominance Index"
        })
        st.dataframe(t1, use_container_width=True)
    else:
        st.info("Required columns missing for Top Artists table.")

    st.markdown('<p class="section-header">🎵 Top Songs Per Artist</p>', unsafe_allow_html=True)
    all_artists = sorted(df["artist"].dropna().unique().tolist())
    if all_artists:
        selected_artist = st.selectbox("Select an artist to view their top songs", options=all_artists)
        artist_songs = df[df["artist"] == selected_artist]
        
        req2 = {"song", "best_rank", "days_on_chart", "popularity"}
        if req2.issubset(artist_songs.columns):
            t2 = (
                artist_songs[list(req2)]
                .drop_duplicates("song")
                .sort_values(["best_rank", "days_on_chart"], ascending=[True, False])
                .reset_index(drop=True)
            )
            t2.index += 1
            t2["popularity"] = t2["popularity"].round(1)
            t2 = t2.rename(columns={
                "song": "Song",
                "best_rank": "Best Rank",
                "days_on_chart": "Days on Chart",
                "popularity": "Popularity",
            })
            st.dataframe(t2, use_container_width=True)
        else:
            st.info("Required columns missing for Top Songs table.")


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------


def render_footer() -> None:
    st.markdown(
        '<div class="dashboard-footer">'
        "Developed using <strong>Streamlit</strong> + <strong>Plotly</strong> + <strong>Pandas</strong>"
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    st.title("🎤 Artist Performance Analysis")
    st.markdown(
        "Analyse the **most dominant artists**, their average popularity, total chart days, "
        "and track their timeline of appearances on the United States Top 50."
    )
    st.divider()

    try:
        df_full = load_pipeline()
    except Exception as exc:
        st.error(f"**Error loading data.** {exc}")
        st.stop()

    df = render_sidebar(df_full)

    if df.empty:
        st.warning("⚠️ No records match the current filters.")
        render_footer()
        return

    render_kpis(df)
    st.divider()
    render_charts(df)
    st.divider()
    render_tables(df)
    render_footer()


if __name__ == "__main__" or True:
    main()
