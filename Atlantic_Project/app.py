"""
app.py
------
Entry point for the United States Top 50 Playlist Performance and
Song Popularity Trend Analysis dashboard.

This module is responsible for:
- Configuring the Streamlit page.
- Loading and caching the full data pipeline (load → preprocess → feature engineer).
- Rendering the sidebar with dataset statistics and interactive filters.
- Applying all sidebar filters to produce a filtered DataFrame.
- Displaying top-level KPI cards and a filtered data preview.

Analysis charts are intentionally excluded from this file; they live inside
the individual pages under the ``pages/`` directory.
"""

import sys
import os

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Path setup — allow ``utils.*`` imports when running from the project root
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))

from utils.loader import load_data
from utils.preprocessing import preprocess_data
from utils.feature_engineering import feature_engineering

# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="United States Top 50 Playlist Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — subtle premium styling
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
        /* Main background */
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
        }

        /* KPI card styling */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1a1d27 0%, #16213e 100%);
            border: 1px solid #2d3561;
            border-radius: 12px;
            padding: 18px 22px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        div[data-testid="metric-container"] label {
            color: #a0aec0 !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase;
        }
        div[data-testid="metric-container"] [data-testid="metric-value"] {
            color: #e2e8f0 !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
        }

        /* Sidebar header */
        [data-testid="stSidebar"] {
            background-color: #0d1117;
            border-right: 1px solid #1e2432;
        }

        /* Footer */
        .dashboard-footer {
            text-align: center;
            color: #4a5568;
            font-size: 0.78rem;
            padding: 28px 0 12px 0;
            border-top: 1px solid #1e2432;
            margin-top: 40px;
        }

        /* Section divider */
        hr {
            border-color: #1e2432 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data pipeline — cached so it only runs once per session
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner="Loading and preparing data…")
def load_pipeline() -> pd.DataFrame:
    """Execute the full data pipeline and return the enriched DataFrame.

    Pipeline
    --------
    1. ``load_data()``          — reads ``data/Atlantic_United_States.csv``
    2. ``preprocess_data()``    — cleans and validates the raw DataFrame
    3. ``feature_engineering()`` — derives 16 analytical columns

    Returns
    -------
    pd.DataFrame
        Fully enriched DataFrame ready for filtering and analysis.

    Raises
    ------
    Any exception raised by the underlying pipeline steps is propagated to
    the caller, which wraps the call in a ``try / except`` and displays a
    Streamlit error message.
    """
    raw = load_data()
    clean = preprocess_data(raw)
    enriched = feature_engineering(clean)
    return enriched


# ---------------------------------------------------------------------------
# Sidebar — statistics + filters
# ---------------------------------------------------------------------------


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Render the sidebar with dataset statistics and interactive filters.

    Parameters
    ----------
    df : pd.DataFrame
        The fully enriched DataFrame from :func:`load_pipeline`.

    Returns
    -------
    pd.DataFrame
        A filtered copy of *df* after applying all sidebar controls.
    """
    with st.sidebar:

        # ---- Dashboard title ------------------------------------------------
        st.markdown("## 🎵 US Top 50 Dashboard")
        st.markdown("*Atlantic Music Analytics*")
        st.divider()

        # ---- Dataset statistics --------------------------------------------
        st.markdown("### 📊 Dataset Statistics")

        date_min = df["date"].min()
        date_max = df["date"].max()

        st.markdown(
            f"""
            | Metric | Value |
            |---|---|
            | **Total Records** | {len(df):,} |
            | **Total Songs** | {df["song"].nunique():,} |
            | **Total Artists** | {df["artist"].nunique():,} |
            | **Date Range** | {date_min.strftime("%d %b %Y")} – {date_max.strftime("%d %b %Y")} |
            """
        )
        st.divider()

        # ---- Filters --------------------------------------------------------
        st.markdown("### 🎚️ Filters")

        # Date range picker
        selected_dates = st.date_input(
            "📅 Date Range",
            value=(date_min.date(), date_max.date()),
            min_value=date_min.date(),
            max_value=date_max.date(),
            help="Filter records to a specific date window.",
        )
        # Unpack safely — user may select only a start date
        if isinstance(selected_dates, (list, tuple)) and len(selected_dates) == 2:
            start_date, end_date = pd.Timestamp(selected_dates[0]), pd.Timestamp(selected_dates[1])
        else:
            start_date = end_date = pd.Timestamp(selected_dates[0])

        # Artist multiselect
        all_artists = sorted(df["artist"].dropna().unique().tolist())
        selected_artists = st.multiselect(
            "🎤 Artist",
            options=all_artists,
            default=[],
            placeholder="All artists",
            help="Leave empty to include all artists.",
        )

        # Song multiselect
        all_songs = sorted(df["song"].dropna().unique().tolist())
        selected_songs = st.multiselect(
            "🎵 Song",
            options=all_songs,
            default=[],
            placeholder="All songs",
            help="Leave empty to include all songs.",
        )

        # Rank slider
        rank_range = st.slider(
            "📈 Playlist Position",
            min_value=1,
            max_value=50,
            value=(1, 50),
            step=1,
            help="Filter by chart position range.",
        )

        # Album type multiselect
        if "album_type" in df.columns:
            all_album_types = sorted(df["album_type"].dropna().unique().tolist())
            selected_album_types = st.multiselect(
                "💿 Album Type",
                options=all_album_types,
                default=[],
                placeholder="All album types",
            )
        else:
            selected_album_types = []

        # Explicit toggle
        explicit_choice = st.radio(
            "🔞 Explicit Content",
            options=["All", "Explicit Only", "Non-Explicit Only"],
            index=0,
            horizontal=True,
        )

    # ---- Apply filters to DataFrame ----------------------------------------
    filtered = df.copy()

    # Date range
    filtered = filtered[
        (filtered["date"] >= start_date) & (filtered["date"] <= end_date)
    ]

    # Artist
    if selected_artists:
        filtered = filtered[filtered["artist"].isin(selected_artists)]

    # Song
    if selected_songs:
        filtered = filtered[filtered["song"].isin(selected_songs)]

    # Position / rank
    filtered = filtered[
        (filtered["position"] >= rank_range[0]) & (filtered["position"] <= rank_range[1])
    ]

    # Album type
    if selected_album_types and "album_type" in filtered.columns:
        filtered = filtered[filtered["album_type"].isin(selected_album_types)]

    # Explicit
    if "is_explicit" in filtered.columns:
        if explicit_choice == "Explicit Only":
            filtered = filtered[filtered["is_explicit"] == True]  # noqa: E712
        elif explicit_choice == "Non-Explicit Only":
            filtered = filtered[filtered["is_explicit"] == False]  # noqa: E712

    return filtered.reset_index(drop=True)


# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------


def render_kpis(df: pd.DataFrame) -> None:
    """Display six KPI metric cards summarising the filtered dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered DataFrame to compute metrics from.
    """
    total_songs = df["song"].nunique() if "song" in df.columns else 0
    total_artists = df["artist"].nunique() if "artist" in df.columns else 0
    avg_popularity = (
        round(df["popularity"].mean(), 1) if "popularity" in df.columns else "N/A"
    )
    avg_rank = round(df["position"].mean(), 1) if "position" in df.columns else "N/A"

    if "is_explicit" in df.columns and len(df) > 0:
        explicit_pct = round(df["is_explicit"].sum() / len(df) * 100, 1)
        explicit_display = f"{explicit_pct}%"
    else:
        explicit_display = "N/A"

    if "chart_longevity" in df.columns:
        avg_longevity = f"{round(df['chart_longevity'].mean(), 1)} days"
    else:
        avg_longevity = "N/A"

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("🎵 Total Songs", f"{total_songs:,}")
    col2.metric("🎤 Total Artists", f"{total_artists:,}")
    col3.metric("⭐ Avg Popularity", avg_popularity)
    col4.metric("📈 Avg Rank", avg_rank)
    col5.metric("🔞 Explicit Songs", explicit_display)
    col6.metric("📅 Avg Chart Longevity", avg_longevity)


# ---------------------------------------------------------------------------
# Data preview table
# ---------------------------------------------------------------------------


def render_preview(df: pd.DataFrame, max_rows: int = 100) -> None:
    """Display a styled preview of the filtered DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered DataFrame to preview.
    max_rows : int, optional
        Maximum number of rows to display (default 100).
    """
    st.markdown(f"### 📋 Data Preview  `({len(df):,} records matching filters)`")

    display_cols = [
        c for c in
        ["date", "song", "artist", "position", "popularity", "album_type",
         "is_explicit", "duration_minutes", "movement", "chart_longevity"]
        if c in df.columns
    ]

    st.dataframe(
        df[display_cols].head(max_rows),
        use_container_width=True,
        hide_index=True,
    )

    if len(df) > max_rows:
        st.caption(f"Showing first {max_rows} of {len(df):,} records.")


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------


def render_footer() -> None:
    """Render a simple branded footer at the bottom of the page."""
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
    """Application entry point — orchestrates all page sections."""

    # ---- Header ------------------------------------------------------------
    st.title("🎵 United States Top 50 Playlist Performance Dashboard")
    st.markdown(
        """
        Explore the **Atlantic United States Top 50** playlist dataset — track chart movements,
        uncover popularity trends, analyse artist dominance, and examine what makes a song
        climb or fall on the charts.  Use the **sidebar filters** to drill into any time period,
        artist, or song you care about.
        """
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

    # ---- Sidebar + filtering -----------------------------------------------
    df_filtered = render_sidebar(df_full)

    # ---- Guard: empty filter result ----------------------------------------
    if df_filtered.empty:
        st.warning(
            "⚠️ No records match the current filters.  "
            "Please adjust the sidebar selections."
        )
        render_footer()
        return

    # ---- KPI cards ---------------------------------------------------------
    render_kpis(df_filtered)
    st.divider()

    # ---- Data preview ------------------------------------------------------
    render_preview(df_filtered)

    # ---- Footer ------------------------------------------------------------
    render_footer()


if __name__ == "__main__" or True:
    main()
