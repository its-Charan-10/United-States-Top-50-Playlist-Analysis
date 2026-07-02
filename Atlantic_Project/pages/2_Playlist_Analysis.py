"""
2_Playlist_Analysis.py
----------------------
Playlist Ranking Analysis page for the United States Top 50 Playlist
Performance and Song Popularity Trend Analysis project.

Sections
--------
1. Sidebar filters (Date Range, Rank, Artist, Song)
2. KPI Cards (6 metrics)
3. Chart Gallery (10 visualisations)
4. Top Fastest Rising Songs table
5. Top Stable Songs table
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
    page_title="Playlist Ranking Analysis",
    page_icon="🎵",
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
    """Execute load → preprocess → feature_engineering pipeline.

    Returns
    -------
    pd.DataFrame
        Fully enriched DataFrame ready for playlist analysis.
    """
    raw = load_data()
    clean = preprocess_data(raw)
    enriched = feature_engineering(clean)
    return enriched


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return the filtered DataFrame.

    Filters applied
    ---------------
    - Date range picker
    - Rank (position) slider 1–50
    - Artist multiselect
    - Song multiselect

    Parameters
    ----------
    df : pd.DataFrame
        Fully enriched DataFrame.

    Returns
    -------
    pd.DataFrame
        Filtered copy of *df*.
    """
    with st.sidebar:
        st.markdown("## 🎵 Playlist Filters")
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

        rank_range = st.slider(
            "📈 Playlist Position",
            min_value=1, max_value=50,
            value=(1, 50), step=1,
        )

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

    # --- Apply filters ---
    filtered = df.copy()
    filtered = filtered[
        (filtered["date"] >= start_date) & (filtered["date"] <= end_date)
    ]
    filtered = filtered[
        (filtered["position"] >= rank_range[0]) & (filtered["position"] <= rank_range[1])
    ]
    if selected_artists:
        filtered = filtered[filtered["artist"].isin(selected_artists)]
    if selected_songs:
        filtered = filtered[filtered["song"].isin(selected_songs)]

    return filtered.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Section 1 — KPI Cards
# ---------------------------------------------------------------------------


def render_kpis(df: pd.DataFrame) -> None:
    """Display 6 playlist-focused KPI metric cards.

    Metrics
    -------
    Average Daily Rank, Highest Rank Achieved, Lowest Rank Achieved,
    Average Rank Volatility, Daily Entries, Daily Exits.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered enriched DataFrame.
    """
    st.markdown('<p class="section-header">📌 Playlist KPIs</p>', unsafe_allow_html=True)

    avg_rank     = round(df["position"].mean(), 1)
    best_rank    = int(df["position"].min())
    worst_rank   = int(df["position"].max())
    avg_vol      = (
        round(df["rank_volatility"].mean(), 2)
        if "rank_volatility" in df.columns else "N/A"
    )

    # Entries = songs appearing for the first time on each date
    if "movement" in df.columns:
        daily_entries = int((df["movement"] == "New Entry").sum())
        daily_exits   = int(
            df.groupby("song")["date"].max().apply(
                lambda d: d < df["date"].max()
            ).sum()
        )
    else:
        daily_entries = daily_exits = "N/A"

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("📈 Avg Daily Rank",       avg_rank)
    c2.metric("🏆 Highest Rank",          f"#{best_rank}")
    c3.metric("📉 Lowest Rank",           f"#{worst_rank}")
    c4.metric("📊 Avg Rank Volatility",   avg_vol)
    c5.metric("🆕 Daily Entries",         f"{daily_entries:,}" if isinstance(daily_entries, int) else daily_entries)
    c6.metric("🚪 Daily Exits",           f"{daily_exits:,}"   if isinstance(daily_exits,   int) else daily_exits)


# ---------------------------------------------------------------------------
# Inline chart helpers (playlist-specific, not in charts.py)
# ---------------------------------------------------------------------------


def _rank_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap of playlist position frequency by date.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``date`` and ``position``.

    Returns
    -------
    go.Figure
    """
    pivot = (
        df.groupby(["date", "position"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    pivot_wide = pivot.pivot(index="position", columns="date", values="count").fillna(0)

    fig = go.Figure(
        go.Heatmap(
            z=pivot_wide.values,
            x=[str(d.date()) for d in pivot_wide.columns],
            y=pivot_wide.index.tolist(),
            colorscale="Viridis",
            hovertemplate="Date: %{x}<br>Position: %{y}<br>Count: %{z}<extra></extra>",
            colorbar=dict(title="Count"),
        )
    )
    fig.update_layout(
        title="Rank Heatmap — Position Frequency by Date",
        xaxis_title="Date",
        yaxis_title="Playlist Position",
        yaxis_autorange="reversed",
        template=_TEMPLATE,
        height=420,
    )
    return fig


def _rank_movement_line(df: pd.DataFrame, top_n: int = 8) -> go.Figure:
    """Multi-line chart of rank over time for the top-N charting songs.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``song``, ``date``, ``position``, ``days_on_chart``.

    Returns
    -------
    go.Figure
    """
    col = "days_on_chart" if "days_on_chart" in df.columns else "position"
    top_songs = (
        df.drop_duplicates("song")
        .nlargest(top_n, col)["song"]
        .tolist()
    )
    subset = df[df["song"].isin(top_songs)].sort_values("date")

    fig = px.line(
        subset,
        x="date", y="position",
        color="song",
        title=f"Rank Movement Over Time — Top {top_n} Songs",
        labels={"date": "Date", "position": "Playlist Position", "song": "Song"},
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        template=_TEMPLATE,
    )
    fig.update_layout(
        yaxis_autorange="reversed",
        xaxis_title="Date",
        yaxis_title="Playlist Position",
        legend_title="Song",
    )
    return fig


def _fastest_rising_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Horizontal bar chart of fastest rising songs by minimum rank change.

    A more negative ``daily_rank_change`` means a bigger upward jump.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``song``, ``daily_rank_change``.

    Returns
    -------
    go.Figure
    """
    if "daily_rank_change" not in df.columns:
        return go.Figure().update_layout(title="daily_rank_change not available")

    rising = (
        df[df["daily_rank_change"] < 0]
        .groupby("song", as_index=False)["daily_rank_change"]
        .min()
        .rename(columns={"daily_rank_change": "best_jump"})
        .nsmallest(top_n, "best_jump")
        .sort_values("best_jump")
    )
    rising["best_jump_abs"] = rising["best_jump"].abs()

    fig = px.bar(
        rising,
        x="best_jump_abs", y="song",
        orientation="h",
        title=f"Fastest Rising Songs — Top {top_n} (Largest Upward Jump)",
        labels={"best_jump_abs": "Positions Gained", "song": "Song"},
        color="best_jump_abs",
        color_continuous_scale="Greens",
        template=_TEMPLATE,
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Positions Gained (Single Day)",
        yaxis_title="Song",
        height=max(380, top_n * 28),
    )
    return fig


def _slowest_declining_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Horizontal bar chart of slowest declining songs.

    Uses the maximum (worst) ``daily_rank_change`` — a large positive value
    means a big downward drop.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``song``, ``daily_rank_change``.

    Returns
    -------
    go.Figure
    """
    if "daily_rank_change" not in df.columns:
        return go.Figure().update_layout(title="daily_rank_change not available")

    declining = (
        df[df["daily_rank_change"] > 0]
        .groupby("song", as_index=False)["daily_rank_change"]
        .max()
        .rename(columns={"daily_rank_change": "worst_drop"})
        .nlargest(top_n, "worst_drop")
        .sort_values("worst_drop", ascending=False)
    )

    fig = px.bar(
        declining,
        x="worst_drop", y="song",
        orientation="h",
        title=f"Slowest Declining Songs — Top {top_n} (Largest Single Drop)",
        labels={"worst_drop": "Positions Lost", "song": "Song"},
        color="worst_drop",
        color_continuous_scale="Reds",
        template=_TEMPLATE,
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Positions Lost (Single Day)",
        yaxis_title="Song",
        height=max(380, top_n * 28),
    )
    return fig


def _rank_volatility_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Bar chart of songs ranked by highest rank volatility.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``song``, ``rank_volatility``.

    Returns
    -------
    go.Figure
    """
    if "rank_volatility" not in df.columns:
        return go.Figure().update_layout(title="rank_volatility not available")

    vol = (
        df[["song", "rank_volatility"]]
        .drop_duplicates("song")
        .dropna(subset=["rank_volatility"])
        .nlargest(top_n, "rank_volatility")
        .sort_values("rank_volatility", ascending=True)
    )

    fig = px.bar(
        vol,
        x="rank_volatility", y="song",
        orientation="h",
        title=f"Top {top_n} Songs by Rank Volatility (Std Dev of Position)",
        labels={"rank_volatility": "Rank Volatility (σ)", "song": "Song"},
        color="rank_volatility",
        color_continuous_scale="Plasma",
        template=_TEMPLATE,
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Rank Volatility (σ)",
        yaxis_title="Song",
        height=max(380, top_n * 28),
    )
    return fig


def _daily_playlist_size_trend(df: pd.DataFrame) -> go.Figure:
    """Line chart showing the number of unique songs on the chart per day.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``date`` and ``song``.

    Returns
    -------
    go.Figure
    """
    daily_size = (
        df.groupby("date", as_index=False)["song"]
        .nunique()
        .rename(columns={"song": "unique_songs"})
        .sort_values("date")
    )

    fig = px.line(
        daily_size,
        x="date", y="unique_songs",
        title="Daily Playlist Size — Unique Songs per Day",
        labels={"date": "Date", "unique_songs": "Unique Songs"},
        markers=True,
        color_discrete_sequence=["#00c8ff"],
        template=_TEMPLATE,
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Unique Songs on Chart")
    return fig


# ---------------------------------------------------------------------------
# Section 2 — Chart Gallery
# ---------------------------------------------------------------------------


def render_charts(df: pd.DataFrame) -> None:
    """Render all 10 playlist-analysis visualisations.

    Charts from charts.py are called directly; page-specific charts use
    the inline helpers defined above.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered enriched DataFrame.
    """
    st.markdown('<p class="section-header">📊 Visualisations</p>', unsafe_allow_html=True)

    # Row 1 — Rank Distribution | Daily Avg Rank Trend
    c1, c2 = st.columns(2)
    with c1:
        try:
            st.plotly_chart(charts.rank_distribution_chart(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Rank Distribution: {exc}")
    with c2:
        try:
            st.plotly_chart(charts.daily_rank_trend(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Daily Rank Trend: {exc}")

    # Row 2 — Rank Heatmap (full width)
    try:
        st.plotly_chart(_rank_heatmap(df), use_container_width=True)
    except Exception as exc:
        st.warning(f"Rank Heatmap: {exc}")

    # Row 3 — Rank Movement Line Chart (full width)
    try:
        st.plotly_chart(_rank_movement_line(df), use_container_width=True)
    except Exception as exc:
        st.warning(f"Rank Movement Line: {exc}")

    # Row 4 — Fastest Rising | Slowest Declining
    c3, c4 = st.columns(2)
    with c3:
        try:
            st.plotly_chart(_fastest_rising_chart(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Fastest Rising: {exc}")
    with c4:
        try:
            st.plotly_chart(_slowest_declining_chart(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Slowest Declining: {exc}")

    # Row 5 — Rank Volatility | Daily Playlist Size
    c5, c6 = st.columns(2)
    with c5:
        try:
            st.plotly_chart(_rank_volatility_chart(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Rank Volatility: {exc}")
    with c6:
        try:
            st.plotly_chart(_daily_playlist_size_trend(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Daily Playlist Size: {exc}")

    # Row 6 — Movement Pie | Rank Frequency Histogram
    c7, c8 = st.columns(2)
    with c7:
        try:
            st.plotly_chart(charts.movement_pie_chart(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Movement Pie: {exc}")
    with c8:
        try:
            st.plotly_chart(charts.rank_distribution_chart(df), use_container_width=True)
        except Exception as exc:
            st.warning(f"Rank Frequency Histogram: {exc}")


# ---------------------------------------------------------------------------
# Section 3 — Top Fastest Rising Songs table
# ---------------------------------------------------------------------------


def render_fastest_rising_table(df: pd.DataFrame, top_n: int = 10) -> None:
    """Display a ranked table of the fastest rising songs.

    Sorted by ``best_rank`` ascending then ``average_rank`` ascending.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame.
    top_n : int, optional
        Number of rows to show (default 10).
    """
    st.markdown('<p class="section-header">🚀 Top Fastest Rising Songs</p>', unsafe_allow_html=True)

    required = {"song", "artist", "best_rank", "average_rank"}
    if not required.issubset(df.columns):
        st.info(f"Missing columns for table: {required - set(df.columns)}")
        return

    # Filter to only "Rising" rows if available
    if "movement" in df.columns:
        rising_df = df[df["movement"] == "Rising"]
    else:
        rising_df = df

    table = (
        rising_df[["song", "artist", "best_rank", "average_rank"]]
        .drop_duplicates("song")
        .nsmallest(top_n, "best_rank")
        .reset_index(drop=True)
    )
    table.index += 1

    if "movement" in df.columns:
        table["movement"] = "Rising"

    table = table.rename(columns={
        "song":         "Song",
        "artist":       "Artist",
        "best_rank":    "Best Rank",
        "average_rank": "Average Rank",
        "movement":     "Movement",
    })
    table["Average Rank"] = table["Average Rank"].round(1)

    st.dataframe(table, use_container_width=True)


# ---------------------------------------------------------------------------
# Section 4 — Top Stable Songs table
# ---------------------------------------------------------------------------


def render_stable_songs_table(df: pd.DataFrame, top_n: int = 10) -> None:
    """Display a ranked table of the most stable (low-volatility) songs.

    Sorted by ``rank_volatility`` ascending (most stable first).

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame.
    top_n : int, optional
        Number of rows to show (default 10).
    """
    st.markdown('<p class="section-header">⚓ Top Stable Songs</p>', unsafe_allow_html=True)

    required = {"song", "rank_volatility", "days_on_chart", "average_rank"}
    if not required.issubset(df.columns):
        st.info(f"Missing columns for table: {required - set(df.columns)}")
        return

    table = (
        df[["song", "rank_volatility", "days_on_chart", "average_rank"]]
        .drop_duplicates("song")
        .dropna(subset=["rank_volatility"])
        .nsmallest(top_n, "rank_volatility")
        .reset_index(drop=True)
    )
    table.index += 1

    table = table.rename(columns={
        "song":            "Song",
        "rank_volatility": "Rank Volatility",
        "days_on_chart":   "Days on Chart",
        "average_rank":    "Average Rank",
    })
    table["Rank Volatility"] = table["Rank Volatility"].round(3)
    table["Average Rank"]    = table["Average Rank"].round(1)

    st.dataframe(table, use_container_width=True)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------


def render_footer() -> None:
    """Render the branded page footer."""
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
    """Orchestrate the Playlist Ranking Analysis page."""

    st.title("🎵 Playlist Ranking Analysis")
    st.markdown(
        "Deep-dive into **daily chart movements**, position volatility, "
        "rising and declining songs, and overall playlist dynamics across "
        "the United States Top 50."
    )
    st.divider()

    # ---- Load data ---------------------------------------------------------
    try:
        df_full = load_pipeline()
    except FileNotFoundError as exc:
        st.error(f"**Dataset not found.** {exc}")
        st.stop()
    except ValueError as exc:
        st.error(f"**Data validation error.** {exc}")
        st.stop()
    except Exception as exc:
        st.error(f"**Unexpected error while loading data.** {exc}")
        st.stop()

    # ---- Sidebar + filter --------------------------------------------------
    df = render_sidebar(df_full)

    if df.empty:
        st.warning("⚠️ No records match the current filters. Adjust the sidebar selections.")
        render_footer()
        return

    # ---- Sections ----------------------------------------------------------
    render_kpis(df)
    st.divider()

    render_charts(df)
    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        render_fastest_rising_table(df)
    with col_right:
        render_stable_songs_table(df)

    render_footer()


if __name__ == "__main__" or True:
    main()
