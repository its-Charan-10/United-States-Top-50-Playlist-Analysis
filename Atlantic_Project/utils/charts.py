"""
charts.py
---------
Reusable Plotly chart functions for the Atlantic Music Analytics dashboard.

Every function in this module:
- Accepts a pandas DataFrame as its primary input.
- Returns a :class:`plotly.graph_objects.Figure` object.
- Never calls ``st.plotly_chart()`` — rendering is the caller's responsibility.
- Never mutates the input DataFrame.
- Validates inputs and raises descriptive exceptions on bad data.

Typical usage
-------------
>>> from utils.charts import rank_distribution_chart
>>> fig = rank_distribution_chart(df)
>>> st.plotly_chart(fig, use_container_width=True)
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------

_TEMPLATE: str = "plotly_dark"
_COLOR_SEQ: list[str] = px.colors.qualitative.Vivid

# ---------------------------------------------------------------------------
# Internal utilities
# ---------------------------------------------------------------------------


def _require_columns(df: pd.DataFrame, *columns: str, fn_name: str = "") -> None:
    """Raise ``ValueError`` if any of *columns* are absent from *df*.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to inspect.
    *columns : str
        Column names that must be present.
    fn_name : str, optional
        Caller function name included in the error message for context.

    Raises
    ------
    TypeError
        If *df* is not a :class:`pandas.DataFrame`.
    ValueError
        If *df* is empty, or if any required column is missing.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"{fn_name}: expected a pandas DataFrame, got {type(df).__name__!r}."
        )
    if df.empty:
        raise ValueError(f"{fn_name}: the input DataFrame is empty.")

    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(
            f"{fn_name}: missing required column(s) {missing}. "
            f"Available: {df.columns.tolist()}"
        )


def _require_song(df: pd.DataFrame, song_name: str, fn_name: str = "") -> pd.DataFrame:
    """Return rows matching *song_name* or raise if none found.

    Parameters
    ----------
    df : pd.DataFrame
        Full chart DataFrame.
    song_name : str
        Song to filter on.
    fn_name : str, optional
        Caller name for error messages.

    Returns
    -------
    pd.DataFrame
        Filtered subset of *df* for *song_name*.

    Raises
    ------
    ValueError
        If *song_name* is not found in the ``song`` column.
    """
    subset = df[df["song"] == song_name]
    if subset.empty:
        raise ValueError(
            f"{fn_name}: song '{song_name}' not found in the dataset. "
            f"Check spelling or choose from df['song'].unique()."
        )
    return subset


# ---------------------------------------------------------------------------
# 1. Rank distribution chart
# ---------------------------------------------------------------------------


def rank_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Histogram of playlist positions across the full dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing a ``position`` column.

    Returns
    -------
    go.Figure
        Plotly histogram figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or ``position`` column is absent.
    """
    _require_columns(df, "position", fn_name="rank_distribution_chart")

    fig = px.histogram(
        df,
        x="position",
        nbins=50,
        title="Distribution of Playlist Positions",
        labels={"position": "Playlist Position", "count": "Frequency"},
        color_discrete_sequence=[_COLOR_SEQ[0]],
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Playlist Position",
        yaxis_title="Frequency",
        bargap=0.05,
    )
    return fig


# ---------------------------------------------------------------------------
# 2. Daily rank trend
# ---------------------------------------------------------------------------


def daily_rank_trend(df: pd.DataFrame) -> go.Figure:
    """Line chart of average playlist rank aggregated by day.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``date`` and ``position`` columns.

    Returns
    -------
    go.Figure
        Plotly line figure with one data point per unique date.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "date", "position", fn_name="daily_rank_trend")

    daily = (
        df.groupby("date", as_index=False)["position"]
        .mean()
        .rename(columns={"position": "avg_position"})
        .sort_values("date")
    )

    fig = px.line(
        daily,
        x="date",
        y="avg_position",
        title="Average Daily Playlist Rank Over Time",
        labels={"date": "Date", "avg_position": "Average Position"},
        markers=True,
        color_discrete_sequence=[_COLOR_SEQ[1]],
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Average Playlist Position",
        yaxis_autorange="reversed",
    )
    return fig


# ---------------------------------------------------------------------------
# 3. Song rank trend
# ---------------------------------------------------------------------------


def song_rank_trend(df: pd.DataFrame, song_name: str) -> go.Figure:
    """Line chart showing a single song's playlist rank over time.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``song``, ``date``, and ``position``.
    song_name : str
        Exact song name to visualise.

    Returns
    -------
    go.Figure
        Plotly line figure for the selected song.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty, required columns are absent, or *song_name* is not
        found.
    """
    _require_columns(df, "song", "date", "position", fn_name="song_rank_trend")
    subset = _require_song(df, song_name, fn_name="song_rank_trend")
    subset = subset.sort_values("date")

    fig = px.line(
        subset,
        x="date",
        y="position",
        title=f"Playlist Rank Over Time — {song_name}",
        labels={"date": "Date", "position": "Playlist Position"},
        markers=True,
        color_discrete_sequence=[_COLOR_SEQ[2]],
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Playlist Position",
        yaxis_autorange="reversed",
    )
    return fig


# ---------------------------------------------------------------------------
# 4. Song popularity trend
# ---------------------------------------------------------------------------


def song_popularity_trend(df: pd.DataFrame, song_name: str) -> go.Figure:
    """Line chart showing a single song's popularity score over time.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``song``, ``date``, and ``popularity``.
    song_name : str
        Exact song name to visualise.

    Returns
    -------
    go.Figure
        Plotly line figure for the selected song.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty, required columns are absent, or *song_name* is not
        found.
    """
    _require_columns(df, "song", "date", "popularity", fn_name="song_popularity_trend")
    subset = _require_song(df, song_name, fn_name="song_popularity_trend")
    subset = subset.sort_values("date")

    fig = px.line(
        subset,
        x="date",
        y="popularity",
        title=f"Popularity Score Over Time — {song_name}",
        labels={"date": "Date", "popularity": "Popularity"},
        markers=True,
        color_discrete_sequence=[_COLOR_SEQ[3]],
        template=_TEMPLATE,
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Popularity Score")
    return fig


# ---------------------------------------------------------------------------
# 5. Top songs — days on chart
# ---------------------------------------------------------------------------


def top_songs_days_on_chart(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """Horizontal bar chart of songs with the longest chart presence.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``song`` and ``days_on_chart`` columns.
        If ``days_on_chart`` is absent it is derived from unique date counts.
    top_n : int, optional
        Number of songs to display (default 20).

    Returns
    -------
    go.Figure
        Plotly horizontal bar figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "song", fn_name="top_songs_days_on_chart")

    if "days_on_chart" in df.columns:
        top = (
            df[["song", "days_on_chart"]]
            .drop_duplicates("song")
            .nlargest(top_n, "days_on_chart")
        )
    else:
        _require_columns(df, "date", fn_name="top_songs_days_on_chart")
        top = (
            df.groupby("song", as_index=False)["date"]
            .nunique()
            .rename(columns={"date": "days_on_chart"})
            .nlargest(top_n, "days_on_chart")
        )

    top = top.sort_values("days_on_chart", ascending=True)

    fig = px.bar(
        top,
        x="days_on_chart",
        y="song",
        orientation="h",
        title=f"Top {top_n} Songs by Days on Chart",
        labels={"days_on_chart": "Days on Chart", "song": "Song"},
        color="days_on_chart",
        color_continuous_scale="Viridis",
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Days on Chart",
        yaxis_title="Song",
        coloraxis_showscale=False,
        height=max(400, top_n * 28),
    )
    return fig


# ---------------------------------------------------------------------------
# 6. Top artists by chart days
# ---------------------------------------------------------------------------


def top_artists_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Bar chart of artists ranked by total unique chart days.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``artist`` and ``date`` columns.
    top_n : int, optional
        Number of artists to display (default 15).

    Returns
    -------
    go.Figure
        Plotly vertical bar figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "artist", "date", fn_name="top_artists_chart")

    if "artist_total_chart_days" in df.columns:
        top = (
            df[["artist", "artist_total_chart_days"]]
            .drop_duplicates("artist")
            .nlargest(top_n, "artist_total_chart_days")
            .rename(columns={"artist_total_chart_days": "chart_days"})
        )
    else:
        top = (
            df.groupby("artist", as_index=False)["date"]
            .nunique()
            .rename(columns={"date": "chart_days"})
            .nlargest(top_n, "chart_days")
        )

    fig = px.bar(
        top,
        x="artist",
        y="chart_days",
        title=f"Top {top_n} Artists by Total Chart Days",
        labels={"artist": "Artist", "chart_days": "Total Chart Days"},
        color="chart_days",
        color_continuous_scale="Plasma",
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Artist",
        yaxis_title="Total Chart Days",
        xaxis_tickangle=-35,
        coloraxis_showscale=False,
    )
    return fig


# ---------------------------------------------------------------------------
# 7. Artist dominance chart
# ---------------------------------------------------------------------------


def artist_dominance_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Bar chart of artists ranked by their dominance index.

    The dominance index equals ``artist_total_chart_days × artist_song_count``.
    If neither pre-computed column exists in *df*, it is derived on the fly.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame.
    top_n : int, optional
        Number of artists to display (default 15).

    Returns
    -------
    go.Figure
        Plotly vertical bar figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "artist", fn_name="artist_dominance_chart")

    if "artist_dominance_index" in df.columns:
        top = (
            df[["artist", "artist_dominance_index"]]
            .drop_duplicates("artist")
            .nlargest(top_n, "artist_dominance_index")
        )
    else:
        _require_columns(df, "song", "date", fn_name="artist_dominance_chart")
        agg = df.groupby("artist", as_index=False).agg(
            chart_days=("date", "nunique"),
            song_count=("song", "nunique"),
        )
        agg["artist_dominance_index"] = agg["chart_days"] * agg["song_count"]
        top = agg.nlargest(top_n, "artist_dominance_index")

    fig = px.bar(
        top,
        x="artist",
        y="artist_dominance_index",
        title=f"Artist Dominance Index — Top {top_n}",
        labels={
            "artist": "Artist",
            "artist_dominance_index": "Dominance Index",
        },
        color="artist_dominance_index",
        color_continuous_scale="Turbo",
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Artist",
        yaxis_title="Dominance Index (Chart Days × Song Count)",
        xaxis_tickangle=-35,
        coloraxis_showscale=False,
    )
    return fig


# ---------------------------------------------------------------------------
# 8. Popularity vs rank scatter
# ---------------------------------------------------------------------------


def popularity_rank_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of popularity versus playlist position coloured by album type.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``popularity``, ``position``, ``album_type``,
        ``song``, and ``artist`` columns.

    Returns
    -------
    go.Figure
        Plotly scatter figure with hover data.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    required = ["popularity", "position", "song", "artist"]
    _require_columns(df, *required, fn_name="popularity_rank_scatter")

    color_col = "album_type" if "album_type" in df.columns else None

    fig = px.scatter(
        df,
        x="popularity",
        y="position",
        color=color_col,
        hover_data={"song": True, "artist": True, "popularity": True, "position": True},
        title="Popularity vs Playlist Position",
        labels={"popularity": "Popularity Score", "position": "Playlist Position"},
        color_discrete_sequence=_COLOR_SEQ,
        opacity=0.7,
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Popularity Score",
        yaxis_title="Playlist Position",
        yaxis_autorange="reversed",
    )
    return fig


# ---------------------------------------------------------------------------
# 9. Popularity distribution
# ---------------------------------------------------------------------------


def popularity_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of popularity scores across the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing a ``popularity`` column.

    Returns
    -------
    go.Figure
        Plotly histogram figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or the ``popularity`` column is absent.
    """
    _require_columns(df, "popularity", fn_name="popularity_distribution")

    fig = px.histogram(
        df,
        x="popularity",
        nbins=40,
        title="Popularity Score Distribution",
        labels={"popularity": "Popularity Score", "count": "Frequency"},
        color_discrete_sequence=[_COLOR_SEQ[4]],
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Popularity Score",
        yaxis_title="Frequency",
        bargap=0.05,
    )
    return fig


# ---------------------------------------------------------------------------
# 10. Explicit vs non-explicit popularity
# ---------------------------------------------------------------------------


def explicit_vs_nonexplicit(df: pd.DataFrame) -> go.Figure:
    """Box plot comparing popularity scores for explicit and non-explicit songs.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``is_explicit`` and ``popularity`` columns.

    Returns
    -------
    go.Figure
        Plotly box figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "is_explicit", "popularity", fn_name="explicit_vs_nonexplicit")

    plot_df = df.copy()
    plot_df["Explicit"] = plot_df["is_explicit"].map(
        {True: "Explicit", False: "Non-Explicit", 1: "Explicit", 0: "Non-Explicit"}
    ).fillna("Unknown")

    fig = px.box(
        plot_df,
        x="Explicit",
        y="popularity",
        color="Explicit",
        title="Popularity: Explicit vs Non-Explicit Songs",
        labels={"Explicit": "Content Type", "popularity": "Popularity Score"},
        color_discrete_sequence=_COLOR_SEQ,
        template=_TEMPLATE,
        points="outliers",
    )
    fig.update_layout(xaxis_title="Content Type", yaxis_title="Popularity Score")
    return fig


# ---------------------------------------------------------------------------
# 11. Album type popularity comparison
# ---------------------------------------------------------------------------


def album_type_comparison(df: pd.DataFrame) -> go.Figure:
    """Box plot comparing popularity scores broken down by album type.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``album_type`` and ``popularity`` columns.

    Returns
    -------
    go.Figure
        Plotly box figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "album_type", "popularity", fn_name="album_type_comparison")

    fig = px.box(
        df,
        x="album_type",
        y="popularity",
        color="album_type",
        title="Popularity by Album Type",
        labels={"album_type": "Album Type", "popularity": "Popularity Score"},
        color_discrete_sequence=_COLOR_SEQ,
        template=_TEMPLATE,
        points="outliers",
    )
    fig.update_layout(
        xaxis_title="Album Type",
        yaxis_title="Popularity Score",
        showlegend=False,
    )
    return fig


# ---------------------------------------------------------------------------
# 12. Duration vs popularity
# ---------------------------------------------------------------------------


def duration_vs_popularity(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of track duration (minutes) against popularity.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``duration_minutes`` and ``popularity``.
        If ``duration_minutes`` is absent but ``duration_ms`` is present, it
        is computed on the fly.

    Returns
    -------
    go.Figure
        Plotly scatter figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "popularity", fn_name="duration_vs_popularity")

    plot_df = df.copy()
    if "duration_minutes" not in plot_df.columns:
        _require_columns(df, "duration_ms", fn_name="duration_vs_popularity")
        plot_df["duration_minutes"] = plot_df["duration_ms"] / 60_000

    hover_cols = {c: True for c in ("song", "artist") if c in plot_df.columns}

    fig = px.scatter(
        plot_df,
        x="duration_minutes",
        y="popularity",
        hover_data=hover_cols,
        title="Track Duration vs Popularity",
        labels={
            "duration_minutes": "Duration (minutes)",
            "popularity": "Popularity Score",
        },
        color_discrete_sequence=[_COLOR_SEQ[5]],
        opacity=0.65,
        trendline="ols",
        trendline_color_override="#ffffff",
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Duration (minutes)",
        yaxis_title="Popularity Score",
    )
    return fig


# ---------------------------------------------------------------------------
# 13. Duration vs rank
# ---------------------------------------------------------------------------


def duration_vs_rank(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of track duration (minutes) against playlist position.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``duration_minutes`` (or ``duration_ms``)
        and ``position``.

    Returns
    -------
    go.Figure
        Plotly scatter figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "position", fn_name="duration_vs_rank")

    plot_df = df.copy()
    if "duration_minutes" not in plot_df.columns:
        _require_columns(df, "duration_ms", fn_name="duration_vs_rank")
        plot_df["duration_minutes"] = plot_df["duration_ms"] / 60_000

    hover_cols = {c: True for c in ("song", "artist") if c in plot_df.columns}

    fig = px.scatter(
        plot_df,
        x="duration_minutes",
        y="position",
        hover_data=hover_cols,
        title="Track Duration vs Playlist Position",
        labels={
            "duration_minutes": "Duration (minutes)",
            "position": "Playlist Position",
        },
        color_discrete_sequence=[_COLOR_SEQ[6]],
        opacity=0.65,
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Duration (minutes)",
        yaxis_title="Playlist Position",
        yaxis_autorange="reversed",
    )
    return fig


# ---------------------------------------------------------------------------
# 14. Album tracks vs popularity
# ---------------------------------------------------------------------------


def album_tracks_vs_popularity(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of album total tracks count against song popularity.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing ``total_tracks`` and ``popularity``.

    Returns
    -------
    go.Figure
        Plotly scatter figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or required columns are absent.
    """
    _require_columns(df, "total_tracks", "popularity", fn_name="album_tracks_vs_popularity")

    hover_cols = {c: True for c in ("song", "artist") if c in df.columns}

    fig = px.scatter(
        df,
        x="total_tracks",
        y="popularity",
        hover_data=hover_cols,
        title="Album Total Tracks vs Song Popularity",
        labels={
            "total_tracks": "Total Tracks in Album",
            "popularity": "Popularity Score",
        },
        color_discrete_sequence=[_COLOR_SEQ[7]],
        opacity=0.65,
        trendline="ols",
        trendline_color_override="#ffffff",
        template=_TEMPLATE,
    )
    fig.update_layout(
        xaxis_title="Total Tracks in Album",
        yaxis_title="Popularity Score",
    )
    return fig


# ---------------------------------------------------------------------------
# 15. Movement pie chart
# ---------------------------------------------------------------------------


def movement_pie_chart(df: pd.DataFrame) -> go.Figure:
    """Pie chart showing the breakdown of rank movement categories.

    Categories: ``"Rising"``, ``"Falling"``, ``"Stable"``, ``"New Entry"``.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing a ``movement`` column.

    Returns
    -------
    go.Figure
        Plotly pie figure.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or the ``movement`` column is absent.
    """
    _require_columns(df, "movement", fn_name="movement_pie_chart")

    counts = df["movement"].value_counts().reset_index()
    counts.columns = ["movement", "count"]

    category_order = ["Rising", "Stable", "Falling", "New Entry"]
    color_map = {
        "Rising": "#00c853",
        "Stable": "#2979ff",
        "Falling": "#ff1744",
        "New Entry": "#ffd600",
    }

    fig = px.pie(
        counts,
        names="movement",
        values="count",
        title="Chart Movement Breakdown",
        color="movement",
        color_discrete_map=color_map,
        category_orders={"movement": category_order},
        template=_TEMPLATE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


# ---------------------------------------------------------------------------
# 16. Correlation heatmap
# ---------------------------------------------------------------------------


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap of Pearson correlations between key numeric features.

    Features used (when present):
    ``popularity``, ``position``, ``duration_minutes``, ``total_tracks``,
    ``average_rank``, ``rank_volatility``.

    Parameters
    ----------
    df : pd.DataFrame
        Chart DataFrame containing at least two of the above numeric columns.

    Returns
    -------
    go.Figure
        Plotly heatmap figure built with :class:`plotly.graph_objects.Heatmap`.

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* is empty or fewer than two of the expected columns are
        available for correlation.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"correlation_heatmap: expected a pandas DataFrame, "
            f"got {type(df).__name__!r}."
        )
    if df.empty:
        raise ValueError("correlation_heatmap: the input DataFrame is empty.")

    desired = [
        "popularity",
        "position",
        "duration_minutes",
        "total_tracks",
        "average_rank",
        "rank_volatility",
    ]
    available = [c for c in desired if c in df.columns]

    if len(available) < 2:
        raise ValueError(
            f"correlation_heatmap: need at least 2 numeric columns from "
            f"{desired}, but only found {available}."
        )

    corr = df[available].corr().round(2)

    fig = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=corr.values,
            texttemplate="%{text:.2f}",
            hovertemplate="x: %{x}<br>y: %{y}<br>correlation: %{z:.2f}<extra></extra>",
            colorbar=dict(title="Pearson r"),
        )
    )
    fig.update_layout(
        title="Feature Correlation Heatmap",
        xaxis_title="Feature",
        yaxis_title="Feature",
        template=_TEMPLATE,
        height=520,
    )
    return fig
