"""
3_Song_Analysis.py
------------------
Song Performance Analysis page for the United States Top 50 Playlist
Performance and Song Popularity Trend Analysis project.

Sections
--------
1. Sidebar filters (Song, Artist, Date Range, Album Type)
2. KPI Cards (5 metrics)
3. Chart Gallery (10 visualisations)
4. Top 20 Songs table
5. Top 20 Popular Songs table
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
    page_title="Song Performance Analysis",
    page_icon="🎼",
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
        st.markdown("## 🎼 Song Filters")
        st.divider()

        all_songs = sorted(df["song"].dropna().unique().tolist())
        selected_songs = st.multiselect(
            "🎵 Song", options=all_songs,
            default=[], placeholder="All songs",
        )

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

    # Apply filters
    filtered = df.copy()
    if selected_songs:
        filtered = filtered[filtered["song"].isin(selected_songs)]
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
    st.markdown('<p class="section-header">📌 Song KPIs</p>', unsafe_allow_html=True)

    # Longest Charting Song
    longest_song = "N/A"
    if "days_on_chart" in df.columns and not df.empty:
        top_l = df.nlargest(1, "days_on_chart")
        if not top_l.empty:
            longest_song = f"{top_l.iloc[0]['song']} ({int(top_l.iloc[0]['days_on_chart'])} days)"

    # Highest Popularity Song
    highest_pop_song = "N/A"
    if "popularity" in df.columns and not df.empty:
        top_p = df.nlargest(1, "popularity")
        if not top_p.empty:
            highest_pop_song = f"{top_p.iloc[0]['song']} ({top_p.iloc[0]['popularity']})"

    # Best Ranked Song (min position)
    best_ranked_song = "N/A"
    if "position" in df.columns and not df.empty:
        best_r = df.nsmallest(1, "position")
        if not best_r.empty:
            best_ranked_song = f"{best_r.iloc[0]['song']} (#{int(best_r.iloc[0]['position'])})"

    # Average Song Popularity
    avg_pop = round(df["popularity"].mean(), 1) if "popularity" in df.columns else "N/A"

    # Average Chart Longevity
    avg_longevity = (
        f"{round(df.drop_duplicates('song')['days_on_chart'].mean(), 1)} days"
        if "days_on_chart" in df.columns else "N/A"
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📅 Longest Charting", longest_song)
    c2.metric("🔥 Highest Popularity", highest_pop_song)
    c3.metric("🏆 Best Ranked", best_ranked_song)
    c4.metric("⭐ Avg Popularity", avg_pop)
    c5.metric("⏳ Avg Longevity", avg_longevity)


# ---------------------------------------------------------------------------
# Inline chart helpers
# ---------------------------------------------------------------------------


def _longevity_vs_peak_rank(df: pd.DataFrame) -> go.Figure:
    if "days_on_chart" not in df.columns or "best_rank" not in df.columns:
        return go.Figure().update_layout(title="Required columns not available")

    agg = df.drop_duplicates("song")
    fig = px.scatter(
        agg,
        x="days_on_chart", y="best_rank",
        hover_data=["song", "artist"],
        title="Longevity vs Peak Rank",
        labels={"days_on_chart": "Days on Chart", "best_rank": "Peak Rank (Best)"},
        color_discrete_sequence=["#ff4081"],
        opacity=0.7,
        template=_TEMPLATE,
    )
    fig.update_layout(yaxis_autorange="reversed")
    return fig


def _daily_popularity_trend(df: pd.DataFrame) -> go.Figure:
    if "popularity" not in df.columns or "date" not in df.columns:
        return go.Figure()
    
    daily = df.groupby("date", as_index=False)["popularity"].mean()
    fig = px.line(
        daily, x="date", y="popularity",
        title="Average Daily Popularity Trend (All Filtered Songs)",
        labels={"date": "Date", "popularity": "Avg Popularity"},
        markers=True,
        color_discrete_sequence=["#00e676"],
        template=_TEMPLATE,
    )
    return fig


def _rolling_popularity_trend(df: pd.DataFrame) -> go.Figure:
    if "popularity_trend" not in df.columns or "date" not in df.columns:
        return go.Figure()
    
    # We can plot the average rolling popularity across all songs per day
    daily = df.groupby("date", as_index=False)["popularity_trend"].mean()
    fig = px.line(
        daily, x="date", y="popularity_trend",
        title="7-Day Rolling Popularity Trend (Average)",
        labels={"date": "Date", "popularity_trend": "Rolling Popularity"},
        markers=True,
        color_discrete_sequence=["#2979ff"],
        template=_TEMPLATE,
    )
    return fig


# ---------------------------------------------------------------------------
# Section 2 — Chart Gallery
# ---------------------------------------------------------------------------


def render_charts(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">📊 Visualisations</p>', unsafe_allow_html=True)

    # For song-specific charts, we need to pick a song if there are multiple
    all_songs = df["song"].unique()
    if len(all_songs) > 0:
        st.markdown("**Select a song for detailed trend analysis:**")
        selected_trend_song = st.selectbox("Song", options=all_songs, label_visibility="collapsed")
    else:
        selected_trend_song = None

    c1, c2 = st.columns(2)
    with c1:
        if selected_trend_song:
            try:
                st.plotly_chart(charts.song_rank_trend(df, selected_trend_song), use_container_width=True)
            except Exception as e:
                st.warning(f"Song Rank Trend: {e}")
        else:
            st.info("No songs available to display Rank Trend.")
    with c2:
        if selected_trend_song:
            try:
                st.plotly_chart(charts.song_popularity_trend(df, selected_trend_song), use_container_width=True)
            except Exception as e:
                st.warning(f"Song Popularity Trend: {e}")
        else:
            st.info("No songs available to display Popularity Trend.")

    try:
        st.plotly_chart(charts.top_songs_days_on_chart(df, top_n=20), use_container_width=True)
    except Exception as e:
        st.warning(f"Top Songs by Days on Chart: {e}")

    c3, c4 = st.columns(2)
    with c3:
        try:
            st.plotly_chart(_longevity_vs_peak_rank(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Longevity vs Peak Rank: {e}")
    with c4:
        try:
            st.plotly_chart(charts.popularity_distribution(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity Distribution: {e}")

    c5, c6 = st.columns(2)
    with c5:
        try:
            st.plotly_chart(charts.rank_distribution_chart(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Rank Distribution: {e}")
    with c6:
        try:
            st.plotly_chart(charts.duration_vs_popularity(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Duration vs Popularity: {e}")

    c7, c8 = st.columns(2)
    with c7:
        try:
            st.plotly_chart(charts.duration_vs_rank(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Duration vs Rank: {e}")
    with c8:
        try:
            st.plotly_chart(_daily_popularity_trend(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Daily Popularity Trend: {e}")

    try:
        st.plotly_chart(_rolling_popularity_trend(df), use_container_width=True)
    except Exception as e:
        st.warning(f"Rolling Popularity Trend: {e}")


# ---------------------------------------------------------------------------
# Section 3 & 4 — Tables
# ---------------------------------------------------------------------------


def render_tables(df: pd.DataFrame) -> None:
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<p class="section-header">🏆 Top 20 Songs</p>', unsafe_allow_html=True)
        req1 = {"song", "artist", "days_on_chart", "average_rank", "best_rank", "popularity"}
        if req1.issubset(df.columns):
            t1 = (
                df[list(req1)]
                .drop_duplicates("song")
                .sort_values(["days_on_chart", "average_rank"], ascending=[False, True])
                .head(20)
                .reset_index(drop=True)
            )
            t1.index += 1
            t1["average_rank"] = t1["average_rank"].round(1)
            t1["popularity"] = t1["popularity"].round(1)
            t1 = t1.rename(columns={
                "song": "Song", "artist": "Artist", "days_on_chart": "Days on Chart",
                "average_rank": "Average Rank", "best_rank": "Best Rank", "popularity": "Popularity"
            })
            st.dataframe(t1, use_container_width=True)
        else:
            st.info("Required columns missing.")

    with c2:
        st.markdown('<p class="section-header">🔥 Top 20 Popular Songs</p>', unsafe_allow_html=True)
        req2 = {"song", "popularity", "average_rank", "days_on_chart"}
        if req2.issubset(df.columns):
            t2 = (
                df[list(req2)]
                .drop_duplicates("song")
                .sort_values("popularity", ascending=False)
                .head(20)
                .reset_index(drop=True)
            )
            t2.index += 1
            t2["average_rank"] = t2["average_rank"].round(1)
            t2["popularity"] = t2["popularity"].round(1)
            t2 = t2.rename(columns={
                "song": "Song", "popularity": "Popularity",
                "average_rank": "Average Rank", "days_on_chart": "Days on Chart"
            })
            st.dataframe(t2, use_container_width=True)
        else:
            st.info("Required columns missing.")


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
    st.title("🎼 Song Performance Analysis")
    st.markdown(
        "Deep-dive into individual **song performance**, including chart longevity, "
        "peak positions, popularity trends, and audio feature correlations."
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
