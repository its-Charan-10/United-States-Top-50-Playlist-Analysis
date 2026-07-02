"""
6_Content_Analysis.py
---------------------
Content Attribute Analysis page for the United States Top 50 Playlist
Performance and Song Popularity Trend Analysis project.

Sections
--------
1. Sidebar filters
2. KPI Cards (5 metrics)
3. Chart Gallery (10 visualisations)
4. Album Type Summary table
5. Explicit Summary table
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
    page_title="Content Attribute Analysis",
    page_icon="🎧",
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
_COLOR_SEQ = px.colors.qualitative.Vivid

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
        st.markdown("## 🎧 Content Filters")
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

        explicit_choice = st.radio(
            "🔞 Explicit Content",
            options=["All", "Explicit Only", "Non-Explicit Only"],
            index=0,
        )

    filtered = df.copy()
    filtered = filtered[
        (filtered["date"] >= start_date) & (filtered["date"] <= end_date)
    ]
    if selected_artists:
        filtered = filtered[filtered["artist"].isin(selected_artists)]
    
    if "is_explicit" in filtered.columns:
        if explicit_choice == "Explicit Only":
            filtered = filtered[filtered["is_explicit"] == True]
        elif explicit_choice == "Non-Explicit Only":
            filtered = filtered[filtered["is_explicit"] == False]

    return filtered.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Section 1 — KPI Cards
# ---------------------------------------------------------------------------


def render_kpis(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">📌 Content KPIs</p>', unsafe_allow_html=True)

    explicit_pct = "N/A"
    if "is_explicit" in df.columns and len(df) > 0:
        explicit_pct = f"{round(df['is_explicit'].mean() * 100, 1)}%"

    album_count = "N/A"
    single_count = "N/A"
    if "album_type" in df.columns:
        album_count = len(df[df["album_type"].str.lower() == "album"]["song"].unique())
        single_count = len(df[df["album_type"].str.lower() == "single"]["song"].unique())

    avg_duration = "N/A"
    if "duration_minutes" in df.columns:
        avg_duration = f"{round(df['duration_minutes'].mean(), 2)} min"
        
    avg_album_size = "N/A"
    if "total_tracks" in df.columns:
        avg_album_size = round(df["total_tracks"].mean(), 1)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🔞 Explicit Songs %", explicit_pct)
    c2.metric("💿 Unique Albums", album_count)
    c3.metric("🎵 Unique Singles", single_count)
    c4.metric("⏱️ Avg Duration", avg_duration)
    c5.metric("📦 Avg Album Size", avg_album_size)


# ---------------------------------------------------------------------------
# Inline chart helpers
# ---------------------------------------------------------------------------


def _duration_histogram(df: pd.DataFrame) -> go.Figure:
    if "duration_minutes" not in df.columns:
        return go.Figure()
        
    fig = px.histogram(
        df,
        x="duration_minutes",
        nbins=40,
        title="Track Duration Distribution (Minutes)",
        labels={"duration_minutes": "Duration (min)", "count": "Frequency"},
        color_discrete_sequence=[_COLOR_SEQ[0]],
        template=_TEMPLATE,
    )
    fig.update_layout(bargap=0.05, xaxis_title="Duration (minutes)", yaxis_title="Count")
    return fig


def _duration_boxplot(df: pd.DataFrame) -> go.Figure:
    if "duration_minutes" not in df.columns:
        return go.Figure()
        
    fig = px.box(
        df,
        y="duration_minutes",
        title="Track Duration Spread",
        labels={"duration_minutes": "Duration (min)"},
        color_discrete_sequence=[_COLOR_SEQ[1]],
        template=_TEMPLATE,
        points="all",
    )
    return fig


def _album_size_vs_rank(df: pd.DataFrame) -> go.Figure:
    if "total_tracks" not in df.columns or "position" not in df.columns:
        return go.Figure()

    hover_cols = {c: True for c in ("song", "artist") if c in df.columns}
    
    fig = px.scatter(
        df,
        x="total_tracks", y="position",
        hover_data=hover_cols,
        title="Album Size vs Playlist Rank",
        labels={"total_tracks": "Total Tracks in Album", "position": "Playlist Position"},
        color_discrete_sequence=[_COLOR_SEQ[2]],
        opacity=0.6,
        template=_TEMPLATE,
    )
    fig.update_layout(yaxis_autorange="reversed")
    return fig


def _explicit_pie_chart(df: pd.DataFrame) -> go.Figure:
    if "is_explicit" not in df.columns:
        return go.Figure()
        
    counts = df["is_explicit"].value_counts().reset_index()
    counts.columns = ["is_explicit", "count"]
    counts["label"] = counts["is_explicit"].map({True: "Explicit", False: "Non-Explicit", 1: "Explicit", 0: "Non-Explicit"})

    fig = px.pie(
        counts,
        names="label", values="count",
        title="Explicit Content Breakdown",
        color="label",
        color_discrete_map={"Explicit": "#ff1744", "Non-Explicit": "#00e676"},
        template=_TEMPLATE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def _album_type_pie_chart(df: pd.DataFrame) -> go.Figure:
    if "album_type" not in df.columns:
        return go.Figure()
        
    counts = df["album_type"].value_counts().reset_index()
    counts.columns = ["album_type", "count"]

    fig = px.pie(
        counts,
        names="album_type", values="count",
        title="Album Type Breakdown",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template=_TEMPLATE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


# ---------------------------------------------------------------------------
# Section 2 — Chart Gallery
# ---------------------------------------------------------------------------


def render_charts(df: pd.DataFrame) -> None:
    st.markdown('<p class="section-header">📊 Content Visualisations</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        try:
            st.plotly_chart(charts.explicit_vs_nonexplicit(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Explicit vs Non-Explicit Popularity: {e}")
    with c2:
        try:
            st.plotly_chart(charts.album_type_comparison(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Album Type Comparison: {e}")

    c3, c4 = st.columns(2)
    with c3:
        try:
            st.plotly_chart(_explicit_pie_chart(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Explicit Pie Chart: {e}")
    with c4:
        try:
            st.plotly_chart(_album_type_pie_chart(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Album Type Pie Chart: {e}")

    c5, c6 = st.columns(2)
    with c5:
        try:
            st.plotly_chart(_duration_histogram(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Duration Histogram: {e}")
    with c6:
        try:
            st.plotly_chart(_duration_boxplot(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Duration Box Plot: {e}")

    c7, c8 = st.columns(2)
    with c7:
        try:
            st.plotly_chart(charts.duration_vs_popularity(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Duration vs Popularity: {e}")
    with c8:
        try:
            st.plotly_chart(charts.duration_vs_rank(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Duration vs Rank: {e}")

    c9, c10 = st.columns(2)
    with c9:
        try:
            st.plotly_chart(charts.album_tracks_vs_popularity(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Album Size vs Popularity: {e}")
    with c10:
        try:
            st.plotly_chart(_album_size_vs_rank(df), use_container_width=True)
        except Exception as e:
            st.warning(f"Album Size vs Rank: {e}")


# ---------------------------------------------------------------------------
# Section 3 & 4 — Tables
# ---------------------------------------------------------------------------


def render_tables(df: pd.DataFrame) -> None:
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<p class="section-header">💿 Album Type Summary</p>', unsafe_allow_html=True)
        req = {"album_type", "popularity", "position", "duration_minutes"}
        if req.issubset(df.columns):
            agg = df.groupby("album_type", as_index=False).agg(
                popularity=("popularity", "mean"),
                average_rank=("position", "mean"),
                duration_minutes=("duration_minutes", "mean")
            ).sort_values("popularity", ascending=False)
            
            agg["popularity"] = agg["popularity"].round(1)
            agg["average_rank"] = agg["average_rank"].round(1)
            agg["duration_minutes"] = agg["duration_minutes"].round(2)
            
            st.dataframe(agg.rename(columns={
                "album_type": "Album Type", "popularity": "Average Popularity",
                "average_rank": "Average Rank", "duration_minutes": "Average Duration (min)"
            }), use_container_width=True, hide_index=True)
        else:
            st.info("Missing columns for Album Type Summary.")

    with c2:
        st.markdown('<p class="section-header">🔞 Explicit Content Summary</p>', unsafe_allow_html=True)
        req2 = {"is_explicit", "song", "popularity", "position"}
        if req2.issubset(df.columns):
            agg2 = df.groupby("is_explicit", as_index=False).agg(
                songs=("song", "nunique"),
                popularity=("popularity", "mean"),
                average_rank=("position", "mean")
            )
            agg2["is_explicit"] = agg2["is_explicit"].map({True: "Explicit", False: "Non-Explicit", 1: "Explicit", 0: "Non-Explicit"}).fillna("Unknown")
            agg2["popularity"] = agg2["popularity"].round(1)
            agg2["average_rank"] = agg2["average_rank"].round(1)
            
            st.dataframe(agg2.rename(columns={
                "is_explicit": "Content Type", "songs": "Unique Songs",
                "popularity": "Average Popularity", "average_rank": "Average Rank"
            }), use_container_width=True, hide_index=True)
        else:
            st.info("Missing columns for Explicit Summary.")


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
    st.title("🎧 Content Attribute Analysis")
    st.markdown(
        "Investigate how **song attributes** (like track duration, explicit content, "
        "and album type) impact overall playlist position and popularity scores."
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
