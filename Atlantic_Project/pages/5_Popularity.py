"""
5_Popularity.py
---------------
Popularity Analytics page for the United States Top 50 Playlist
Performance and Song Popularity Trend Analysis project.

Sections
--------
1. Sidebar filters
2. KPI Cards (5 metrics)
3. Chart Gallery (10 visualisations)
4. Top Popular Songs table
5. Bottom Popular Songs table
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
    page_title="Popularity Analytics",
    page_icon="⭐",
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
# Data pipeline
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
        st.markdown("## ⭐ Popularity Filters")
        st.divider()

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

        all_artists = sorted(df["artist"].dropna().unique().tolist())
        selected_artists = st.multiselect(
            "🎤 Artist", options=all_artists,
            default=[], placeholder="All artists",
        )

        all_songs = sorted(df["song"].dropna().unique().tolist())
        selected_songs = st.multiselect(
            "🎵 Song", options=all_songs,
            default=[], placeholder="All songs",
        )

        if "album_type" in df.columns:
            all_album_types = sorted(df["album_type"].dropna().unique().tolist())
            selected_album_types = st.multiselect(
                "💿 Album Type", options=all_album_types,
                default=[], placeholder="All album types",
            )
        else:
            selected_album_types = []

    filtered = df.copy()
    filtered = filtered[
        (filtered["date"] >= start_date) & (filtered["date"] <= end_date)
    ]
    if selected_artists:
        filtered = filtered[filtered["artist"].isin(selected_artists)]
    if selected_songs:
        filtered = filtered[filtered["song"].isin(selected_songs)]
    if selected_album_types and "album_type" in filtered.columns:
        filtered = filtered[filtered["album_type"].isin(selected_album_types)]

    return filtered.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Section 1 — KPI Cards
# ---------------------------------------------------------------------------


def render_kpis(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">📌 Popularity KPIs</p>', unsafe_allow_html=True)

    avg_pop = "N/A"
    high_pop = "N/A"
    low_pop = "N/A"
    std_pop = "N/A"
    corr_rank = "N/A"

    if "popularity" in df.columns and not df.empty:
        avg_pop = round(df["popularity"].mean(), 1)
        high_pop = int(df["popularity"].max())
        low_pop = int(df["popularity"].min())
        std_pop = round(df["popularity"].std(), 2)
        
        if "position" in df.columns:
            corr = df[["popularity", "position"]].corr().iloc[0, 1]
            corr_rank = round(corr, 3)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("⭐ Avg Popularity", avg_pop)
    c2.metric("🔥 Highest Popularity", high_pop)
    c3.metric("❄️ Lowest Popularity", low_pop)
    c4.metric("📊 Popularity Std Dev", std_pop)
    c5.metric("🔗 Rank Correlation", corr_rank)


# ---------------------------------------------------------------------------
# Inline chart helpers
# ---------------------------------------------------------------------------


def _popularity_box_plot(df: pd.DataFrame) -> go.Figure:
    if "popularity" not in df.columns:
        return go.Figure()
        
    fig = px.box(
        df,
        y="popularity",
        title="Popularity Score Box Plot",
        labels={"popularity": "Popularity"},
        color_discrete_sequence=["#ff9800"],
        template=_TEMPLATE,
        points="all",
    )
    return fig


def _rolling_popularity_trend(df: pd.DataFrame) -> go.Figure:
    if "popularity_trend" not in df.columns or "date" not in df.columns:
        return go.Figure()
    
    daily = df.groupby("date", as_index=False)["popularity_trend"].mean()
    fig = px.line(
        daily, x="date", y="popularity_trend",
        title="Rolling Popularity Trend (7-Day Average)",
        labels={"date": "Date", "popularity_trend": "Popularity"},
        markers=True,
        color_discrete_sequence=["#2979ff"],
        template=_TEMPLATE,
    )
    return fig


def _popularity_heatmap(df: pd.DataFrame) -> go.Figure:
    if "popularity" not in df.columns or "date" not in df.columns:
        return go.Figure()

    # Bin popularity into deciles for a heatmap
    df_heat = df.copy()
    df_heat["pop_bin"] = pd.cut(df_heat["popularity"], bins=range(0, 101, 10), right=False)
    
    pivot = (
        df_heat.groupby(["date", "pop_bin"], as_index=False, observed=False)
        .size()
        .rename(columns={"size": "count"})
    )
    
    # Format labels cleanly
    pivot["pop_label"] = pivot["pop_bin"].apply(lambda x: f"{x.left}-{x.right-1}")
    pivot_wide = pivot.pivot(index="pop_label", columns="date", values="count").fillna(0)

    # Sort index by bin intervals
    sorted_labels = [f"{i}-{i+9}" for i in range(0, 100, 10)]
    pivot_wide = pivot_wide.reindex(sorted_labels).fillna(0)

    fig = go.Figure(
        go.Heatmap(
            z=pivot_wide.values,
            x=[str(d.date()) for d in pivot_wide.columns],
            y=pivot_wide.index.tolist(),
            colorscale="Inferno",
            hovertemplate="Date: %{x}<br>Popularity Range: %{y}<br>Count: %{z}<extra></extra>",
            colorbar=dict(title="Count"),
        )
    )
    fig.update_layout(
        title="Popularity Heatmap (Scores vs Date)",
        xaxis_title="Date",
        yaxis_title="Popularity Range",
        template=_TEMPLATE,
        height=420,
    )
    return fig


# ---------------------------------------------------------------------------
# Section 2 — Chart Gallery
# ---------------------------------------------------------------------------


def render_charts(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">📊 Visualisations</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        try:
            st.plotly_chart(charts.popularity_distribution(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity Histogram: {e}")
    with c2:
        try:
            st.plotly_chart(_popularity_box_plot(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity Box Plot: {e}")

    # Full width Heatmap and Line Trend
    try:
        st.plotly_chart(_popularity_heatmap(df), use_container_width=True)
    except Exception as e:
        st.warning(f"Popularity Heatmap: {e}")

    try:
        st.plotly_chart(_rolling_popularity_trend(df), use_container_width=True)
    except Exception as e:
        st.warning(f"Rolling Popularity Trend: {e}")

    c3, c4 = st.columns(2)
    with c3:
        try:
            st.plotly_chart(charts.popularity_rank_scatter(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity vs Rank Scatter: {e}")
    with c4:
        try:
            st.plotly_chart(charts.correlation_heatmap(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Correlation Matrix: {e}")

    c5, c6 = st.columns(2)
    with c5:
        try:
            st.plotly_chart(charts.album_type_comparison(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity by Album Type: {e}")
    with c6:
        try:
            st.plotly_chart(charts.explicit_vs_nonexplicit(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity by Explicit Content: {e}")

    c7, c8 = st.columns(2)
    with c7:
        try:
            st.plotly_chart(charts.duration_vs_popularity(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity vs Duration: {e}")
    with c8:
        try:
            st.plotly_chart(charts.album_tracks_vs_popularity(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Popularity vs Total Tracks: {e}")


# ---------------------------------------------------------------------------
# Section 3 & 4 — Tables
# ---------------------------------------------------------------------------


def render_tables(df: pd.DataFrame) -> None:
    c1, c2 = st.columns(2)
    
    req = {"song", "artist", "popularity", "average_rank"}
    if not req.issubset(df.columns):
        st.info("Missing columns to render popularity tables.")
        return

    # Aggregate to single song records
    agg = df.groupby(["song", "artist"], as_index=False).agg(
        popularity=("popularity", "max"),
        average_rank=("average_rank", "mean")
    )
    agg["average_rank"] = agg["average_rank"].round(1)

    with c1:
        st.markdown('<p class="section-header">🔥 Top Popular Songs</p>', unsafe_allow_html=True)
        top_songs = (
            agg.nlargest(20, "popularity")
            .sort_values(["popularity", "average_rank"], ascending=[False, True])
            .reset_index(drop=True)
        )
        top_songs.index += 1
        st.dataframe(top_songs.rename(columns={
            "song": "Song", "artist": "Artist", 
            "popularity": "Popularity", "average_rank": "Avg Rank"
        }), use_container_width=True)

    with c2:
        st.markdown('<p class="section-header">❄️ Bottom Popular Songs</p>', unsafe_allow_html=True)
        bot_songs = (
            agg.nsmallest(20, "popularity")
            .sort_values(["popularity", "average_rank"], ascending=[True, False])
            .reset_index(drop=True)
        )
        bot_songs.index += 1
        st.dataframe(bot_songs.rename(columns={
            "song": "Song", "artist": "Artist", 
            "popularity": "Popularity", "average_rank": "Avg Rank"
        }), use_container_width=True)


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
    st.title("⭐ Popularity Analytics")
    st.markdown(
        "Analyze the **distribution and trends of popularity scores**, "
        "and explore correlations with chart positions, audio features, and track metadata."
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
