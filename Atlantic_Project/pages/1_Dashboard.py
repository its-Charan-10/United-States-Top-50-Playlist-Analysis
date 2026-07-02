"""
1_Dashboard.py
--------------
Dashboard Overview page for the United States Top 50 Playlist Performance
and Song Popularity Trend Analysis project.

Sections
--------
1. KPI Cards (8 metrics)
2. Chart Gallery (7 visualisations)
3. Top 10 Songs table
4. Top 10 Artists table
5. Project Insights (auto-generated)
6. Dataset Preview (expandable)
"""

import sys
import os

import pandas as pd
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
    page_title="Dashboard Overview",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Shared CSS — mirrors app.py premium styling
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

# ---------------------------------------------------------------------------
# Data pipeline — cached
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner="🔄 Loading and preparing data…")
def load_pipeline() -> pd.DataFrame:
    """Execute load → preprocess → feature_engineering pipeline.

    Returns
    -------
    pd.DataFrame
        Fully enriched DataFrame ready for analysis.

    Raises
    ------
    FileNotFoundError
        Propagated from ``load_data()`` if the CSV is missing.
    ValueError
        Propagated from ``preprocess_data()`` or ``feature_engineering()``.
    RuntimeError
        Propagated for unexpected failures in any pipeline stage.
    """
    raw = load_data()
    clean = preprocess_data(raw)
    enriched = feature_engineering(clean)
    return enriched


# ---------------------------------------------------------------------------
# Section 1 — KPI Cards
# ---------------------------------------------------------------------------


def render_kpis(df: pd.DataFrame) -> None:
    """Render 8 KPI metric cards in two rows of four.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched and (optionally) filtered DataFrame.
    """
    st.markdown('<p class="section-header">📌 Key Performance Indicators</p>', unsafe_allow_html=True)

    total_songs     = df["song"].nunique()
    total_artists   = df["artist"].nunique()
    total_records   = len(df)
    avg_popularity  = round(df["popularity"].mean(), 1) if "popularity" in df.columns else "N/A"
    avg_rank        = round(df["position"].mean(), 1) if "position" in df.columns else "N/A"
    best_rank       = int(df["position"].min()) if "position" in df.columns else "N/A"
    avg_longevity   = (
        f"{round(df['chart_longevity'].mean(), 1)} days"
        if "chart_longevity" in df.columns else "N/A"
    )
    explicit_pct    = (
        f"{round(df['is_explicit'].sum() / len(df) * 100, 1)}%"
        if "is_explicit" in df.columns and len(df) > 0 else "N/A"
    )

    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    r1c1.metric("🎵 Total Songs",          f"{total_songs:,}")
    r1c2.metric("🎤 Total Artists",         f"{total_artists:,}")
    r1c3.metric("📋 Total Records",         f"{total_records:,}")
    r1c4.metric("⭐ Avg Popularity",        avg_popularity)

    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    r2c1.metric("📈 Average Rank",          avg_rank)
    r2c2.metric("🏆 Best Rank Achieved",    f"#{best_rank}")
    r2c3.metric("📅 Avg Chart Longevity",   avg_longevity)
    r2c4.metric("🔞 Explicit Song %",       explicit_pct)


# ---------------------------------------------------------------------------
# Section 2 — Chart Gallery
# ---------------------------------------------------------------------------


def render_charts(df: pd.DataFrame) -> None:
    """Render 7 analysis charts in a professional two-column layout.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame to plot.
    """
    st.markdown('<p class="section-header">📊 Chart Gallery</p>', unsafe_allow_html=True)

    # Row 1 — Rank Distribution | Daily Rank Trend
    col_a, col_b = st.columns(2)
    with col_a:
        try:
            st.plotly_chart(
                charts.rank_distribution_chart(df),
                use_container_width=True,
            )
        except Exception as exc:
            st.warning(f"Rank Distribution: {exc}")

    with col_b:
        try:
            st.plotly_chart(
                charts.daily_rank_trend(df),
                use_container_width=True,
            )
        except Exception as exc:
            st.warning(f"Daily Rank Trend: {exc}")

    # Row 2 — Top 20 Songs (full width — horizontal bar benefits from space)
    try:
        st.plotly_chart(
            charts.top_songs_days_on_chart(df, top_n=20),
            use_container_width=True,
        )
    except Exception as exc:
        st.warning(f"Top Songs Chart: {exc}")

    # Row 3 — Top 15 Artists | Popularity Distribution
    col_c, col_d = st.columns(2)
    with col_c:
        try:
            st.plotly_chart(
                charts.top_artists_chart(df, top_n=15),
                use_container_width=True,
            )
        except Exception as exc:
            st.warning(f"Top Artists Chart: {exc}")

    with col_d:
        try:
            st.plotly_chart(
                charts.popularity_distribution(df),
                use_container_width=True,
            )
        except Exception as exc:
            st.warning(f"Popularity Distribution: {exc}")

    # Row 4 — Popularity vs Rank Scatter | Movement Pie
    col_e, col_f = st.columns(2)
    with col_e:
        try:
            st.plotly_chart(
                charts.popularity_rank_scatter(df),
                use_container_width=True,
            )
        except Exception as exc:
            st.warning(f"Popularity vs Rank Scatter: {exc}")

    with col_f:
        try:
            st.plotly_chart(
                charts.movement_pie_chart(df),
                use_container_width=True,
            )
        except Exception as exc:
            st.warning(f"Movement Pie Chart: {exc}")


# ---------------------------------------------------------------------------
# Section 3 — Top 10 Songs table
# ---------------------------------------------------------------------------


def render_top_songs(df: pd.DataFrame) -> None:
    """Display a ranked table of the top 10 songs by chart presence.

    Sorted by ``days_on_chart`` (desc) then ``average_rank`` (asc).

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame.
    """
    st.markdown('<p class="section-header">🎵 Top 10 Songs</p>', unsafe_allow_html=True)

    required = {"song", "artist", "days_on_chart", "average_rank", "best_rank", "popularity"}
    missing = required - set(df.columns)
    if missing:
        st.info(f"Columns not available for Top Songs table: {missing}")
        return

    top_songs = (
        df[list(required)]
        .drop_duplicates(subset="song")
        .sort_values(["days_on_chart", "average_rank"], ascending=[False, True])
        .head(10)
        .reset_index(drop=True)
    )
    top_songs.index += 1  # 1-based rank

    top_songs = top_songs.rename(columns={
        "song":          "Song",
        "artist":        "Artist",
        "days_on_chart": "Days on Chart",
        "average_rank":  "Average Rank",
        "best_rank":     "Best Rank",
        "popularity":    "Popularity",
    })
    top_songs["Average Rank"] = top_songs["Average Rank"].round(1)
    top_songs["Popularity"]   = top_songs["Popularity"].round(1)

    st.dataframe(top_songs, use_container_width=True)


# ---------------------------------------------------------------------------
# Section 4 — Top 10 Artists table
# ---------------------------------------------------------------------------


def render_top_artists(df: pd.DataFrame) -> None:
    """Display a ranked table of the top 10 artists by dominance index.

    Sorted by ``artist_dominance_index`` (desc).

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame.
    """
    st.markdown('<p class="section-header">🎤 Top 10 Artists</p>', unsafe_allow_html=True)

    required = {
        "artist",
        "artist_song_count",
        "artist_total_chart_days",
        "artist_average_popularity",
        "artist_dominance_index",
    }
    missing = required - set(df.columns)
    if missing:
        st.info(f"Columns not available for Top Artists table: {missing}")
        return

    top_artists = (
        df[list(required)]
        .drop_duplicates(subset="artist")
        .sort_values("artist_dominance_index", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    top_artists.index += 1  # 1-based rank

    top_artists = top_artists.rename(columns={
        "artist":                    "Artist",
        "artist_song_count":         "Songs",
        "artist_total_chart_days":   "Chart Days",
        "artist_average_popularity": "Avg Popularity",
        "artist_dominance_index":    "Dominance Index",
    })
    top_artists["Avg Popularity"] = top_artists["Avg Popularity"].round(1)

    st.dataframe(top_artists, use_container_width=True)


# ---------------------------------------------------------------------------
# Section 5 — Project Insights
# ---------------------------------------------------------------------------


def render_insights(df: pd.DataFrame) -> None:
    """Auto-generate and display contextual insights from the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame used to derive each insight.
    """
    st.markdown('<p class="section-header">💡 Project Insights</p>', unsafe_allow_html=True)

    insights: list[tuple[str, str]] = []   # (kind, message)

    # Most dominant artist
    if "artist_dominance_index" in df.columns and "artist" in df.columns:
        top_a = df[["artist", "artist_dominance_index"]].drop_duplicates("artist").nlargest(1, "artist_dominance_index")
        if not top_a.empty:
            top_artist_row = top_a.iloc[0]
            insights.append((
                "success",
                f"🏆 **Most Dominant Artist:** {top_artist_row['artist']} "
                f"(Dominance Index: {int(top_artist_row['artist_dominance_index']):,})",
            ))

    # Longest charting song
    if "days_on_chart" in df.columns and "song" in df.columns:
        top_s = df[["song", "artist", "days_on_chart"]].drop_duplicates("song").nlargest(1, "days_on_chart")
        if not top_s.empty:
            top_song_row = top_s.iloc[0]
            insights.append((
                "info",
                f"📅 **Longest Charting Song:** *{top_song_row['song']}* "
                f"by {top_song_row['artist']} "
                f"— {int(top_song_row['days_on_chart'])} days on chart.",
            ))

    # Average popularity
    if "popularity" in df.columns:
        avg_pop = round(df["popularity"].mean(), 1)
        insights.append((
            "info",
            f"⭐ **Average Popularity Score:** {avg_pop} / 100 across all "
            f"{df['song'].nunique():,} unique songs.",
        ))

    # Explicit content percentage
    if "is_explicit" in df.columns and len(df) > 0:
        pct = round(df["is_explicit"].sum() / len(df) * 100, 1)
        level = "warning" if pct > 30 else "info"
        insights.append((
            level,
            f"🔞 **Explicit Content:** {pct}% of chart records are marked explicit.",
        ))

    # Average chart rank
    if "position" in df.columns:
        avg_pos = round(df["position"].mean(), 1)
        insights.append((
            "info",
            f"📈 **Average Playlist Position:** {avg_pos} — songs typically "
            "appear in the middle of the Top 50."
            if 20 <= avg_pos <= 35
            else f"📈 **Average Playlist Position:** {avg_pos} across all chart entries.",
        ))

    # Render
    for kind, message in insights:
        if kind == "success":
            st.success(message)
        elif kind == "warning":
            st.warning(message)
        else:
            st.info(message)


# ---------------------------------------------------------------------------
# Section 6 — Dataset Preview (expandable)
# ---------------------------------------------------------------------------


def render_dataset_preview(df: pd.DataFrame, max_rows: int = 100) -> None:
    """Render an expandable section showing the first N rows of the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame.
    max_rows : int, optional
        Number of rows to display (default 100).
    """
    with st.expander(f"🗂️ Dataset Preview  —  first {max_rows} rows", expanded=False):
        display_cols = [
            c for c in
            [
                "date", "song", "artist", "position", "popularity",
                "album_type", "is_explicit", "duration_minutes",
                "days_on_chart", "movement", "chart_longevity",
                "artist_dominance_index",
            ]
            if c in df.columns
        ]
        st.dataframe(df[display_cols].head(max_rows), use_container_width=True, hide_index=True)
        st.caption(f"Displaying {min(max_rows, len(df)):,} of {len(df):,} total records.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Orchestrate all dashboard sections."""

    # ---- Page header -------------------------------------------------------
    st.title("📊 Dashboard Overview")
    st.markdown(
        "A high-level snapshot of the **United States Top 50 Playlist** — "
        "covering chart activity, artist performance, song longevity, and "
        "popularity trends across the full dataset."
    )
    st.divider()

    # ---- Load data ---------------------------------------------------------
    try:
        df = load_pipeline()
    except FileNotFoundError as exc:
        st.error(f"**Dataset not found.** {exc}")
        st.stop()
    except ValueError as exc:
        st.error(f"**Data validation error.** {exc}")
        st.stop()
    except Exception as exc:
        st.error(f"**Unexpected error while loading data.** {exc}")
        st.stop()

    # ---- Sections ----------------------------------------------------------
    render_kpis(df)
    st.divider()

    render_charts(df)
    st.divider()

    # Top tables side-by-side
    col_left, col_right = st.columns(2)
    with col_left:
        render_top_songs(df)
    with col_right:
        render_top_artists(df)

    st.divider()
    render_insights(df)
    st.divider()
    render_dataset_preview(df)

    # ---- Footer ------------------------------------------------------------
    st.markdown(
        '<div class="dashboard-footer">'
        "Developed using <strong>Streamlit</strong> + <strong>Plotly</strong> + <strong>Pandas</strong>"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__" or True:
    main()
