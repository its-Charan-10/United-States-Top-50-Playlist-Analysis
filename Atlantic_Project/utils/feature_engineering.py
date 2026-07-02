"""
feature_engineering.py
----------------------
Feature engineering utilities for the Atlantic Music Analytics Streamlit app.

This module exposes a single public entry-point, ``feature_engineering()``,
which derives 16 analytical columns from the cleaned DataFrame produced by
``utils.preprocessing.preprocess_data()``.  All helpers are private and
operate on an explicit copy of the input so the caller's DataFrame is never
mutated.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Columns required before feature engineering can proceed.
REQUIRED_COLUMNS: list[str] = ["song", "artist", "date", "popularity", "position"]

#: Window size (in days) used for the rolling popularity trend.
ROLLING_WINDOW_DAYS: int = 7


# ---------------------------------------------------------------------------
# Private helpers — song-level features
# ---------------------------------------------------------------------------


def _add_duration_minutes(df: pd.DataFrame) -> pd.DataFrame:
    """Add ``duration_minutes`` derived from ``duration_ms``.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.  If ``duration_ms`` is absent the column is silently
        skipped and ``duration_minutes`` will not be created.

    Returns
    -------
    pd.DataFrame
        DataFrame with an optional ``duration_minutes`` float column.
    """
    if "duration_ms" in df.columns:
        df["duration_minutes"] = df["duration_ms"] / 60_000
    return df


def _add_song_chart_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Add per-song chart aggregate features via ``groupby`` + ``transform``.

    Features added
    --------------
    days_on_chart : int
        Number of unique dates the song appears.
    average_rank : float
        Mean ``position`` across all appearances.
    best_rank : float
        Minimum (best) ``position`` across all appearances.
    worst_rank : float
        Maximum (worst) ``position`` across all appearances.
    rank_volatility : float
        Standard deviation of ``position`` across all appearances.
    first_chart_date : datetime
        Earliest date the song appeared on the chart.
    last_chart_date : datetime
        Latest date the song appeared on the chart.
    chart_longevity : int
        ``(last_chart_date - first_chart_date).days + 1``.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.  Must contain ``song``, ``date``, and ``position``.

    Returns
    -------
    pd.DataFrame
        DataFrame with the above columns appended.
    """
    grp = df.groupby("song", sort=False)

    df["days_on_chart"] = grp["date"].transform("nunique")
    df["average_rank"] = grp["position"].transform("mean")
    df["best_rank"] = grp["position"].transform("min")
    df["worst_rank"] = grp["position"].transform("max")
    df["rank_volatility"] = grp["position"].transform("std")

    df["first_chart_date"] = grp["date"].transform("min")
    df["last_chart_date"] = grp["date"].transform("max")

    df["chart_longevity"] = (
        (df["last_chart_date"] - df["first_chart_date"]).dt.days + 1
    )

    return df


def _add_popularity_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 7-day rolling average popularity for each song ordered by date.

    The rolling window is time-based (``7D``) and requires ``date`` to be
    the index.  The column is computed per-song via ``groupby`` and the
    result is aligned back onto *df* by original index.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.  Must contain ``song``, ``date``, and ``popularity``.

    Returns
    -------
    pd.DataFrame
        DataFrame with a ``popularity_trend`` float column added.
    """
    # Build a temporary frame indexed by date for the rolling operation.
    tmp = df[["song", "date", "popularity"]].copy().set_index("date").sort_index()

    rolling_series = (
        tmp.groupby("song", sort=False)["popularity"]
        .transform(
            lambda s: s.rolling(f"{ROLLING_WINDOW_DAYS}D", min_periods=1).mean()
        )
    )

    # ``rolling_series`` shares the tmp index; map back to the original index.
    rolling_series.index = df.index
    df["popularity_trend"] = rolling_series
    return df


def _add_daily_rank_change_and_movement(df: pd.DataFrame) -> pd.DataFrame:
    """Add ``daily_rank_change`` and ``movement`` columns.

    Each song's rows are ordered by ``date``; ``daily_rank_change`` is the
    difference between today's ``position`` and the previous day's
    ``position`` for the same song.

    ``movement`` categories
    -----------------------
    - ``"New Entry"``  — no previous rank exists.
    - ``"Rising"``     — rank improved (change < 0, smaller number = better).
    - ``"Falling"``    — rank worsened (change > 0).
    - ``"Stable"``     — rank unchanged (change == 0).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.  Must contain ``song``, ``date``, and ``position``.

    Returns
    -------
    pd.DataFrame
        DataFrame with ``daily_rank_change`` (float) and ``movement`` (str)
        columns appended.
    """
    df = df.sort_values(["song", "date"])

    df["daily_rank_change"] = df.groupby("song", sort=False)["position"].diff()

    def _categorise(change: float) -> str:
        if pd.isna(change):
            return "New Entry"
        if change < 0:
            return "Rising"
        if change > 0:
            return "Falling"
        return "Stable"

    df["movement"] = df["daily_rank_change"].map(_categorise)
    return df


# ---------------------------------------------------------------------------
# Private helpers — artist-level features
# ---------------------------------------------------------------------------


def _add_artist_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Add per-artist aggregate features via ``groupby`` + ``transform``.

    Features added
    --------------
    artist_song_count : int
        Number of unique songs credited to the artist.
    artist_total_chart_days : int
        Total unique chart dates across all of the artist's songs.
    artist_average_popularity : float
        Mean ``popularity`` score across all of the artist's chart entries.
    artist_dominance_index : float
        ``artist_total_chart_days × artist_song_count``.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.  Must contain ``artist``, ``song``, ``date``, and
        ``popularity``.

    Returns
    -------
    pd.DataFrame
        DataFrame with the above columns appended.
    """
    grp = df.groupby("artist", sort=False)

    df["artist_song_count"] = grp["song"].transform("nunique")
    df["artist_total_chart_days"] = grp["date"].transform("nunique")
    df["artist_average_popularity"] = grp["popularity"].transform("mean")

    df["artist_dominance_index"] = (
        df["artist_total_chart_days"] * df["artist_song_count"]
    )

    return df


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def _validate_input(df: pd.DataFrame) -> None:
    """Raise a descriptive error if *df* is invalid or missing required columns.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to validate.

    Raises
    ------
    TypeError
        If *df* is not a :class:`pandas.DataFrame`.
    ValueError
        If *df* is empty, or if any column in :data:`REQUIRED_COLUMNS` is
        absent.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"feature_engineering() expects a pandas DataFrame, "
            f"got {type(df).__name__!r}."
        )
    if df.empty:
        raise ValueError(
            "The input DataFrame is empty — feature engineering cannot proceed."
        )

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"The following required columns are missing: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )

    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        raise ValueError(
            "The 'date' column must be of datetime dtype.  "
            "Run utils.loader.load_data() before calling feature_engineering()."
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Derive analytical features from the cleaned Atlantic music DataFrame.

    Applies the full feature engineering pipeline in the following order:

    **Song-level features**

    1. ``duration_minutes``       — ``duration_ms / 60 000``
    2. ``days_on_chart``          — unique chart dates per song
    3. ``average_rank``           — mean ``position`` per song
    4. ``best_rank``              — minimum ``position`` per song
    5. ``worst_rank``             — maximum ``position`` per song
    6. ``rank_volatility``        — standard deviation of ``position`` per song
    7. ``first_chart_date``       — earliest appearance date per song
    8. ``last_chart_date``        — latest appearance date per song
    9. ``chart_longevity``        — ``(last − first).days + 1`` per song
    10. ``popularity_trend``       — 7-day rolling mean popularity per song
    11. ``daily_rank_change``      — day-over-day position delta per song
    12. ``movement``               — ``"Rising" | "Falling" | "Stable" | "New Entry"``

    **Artist-level features**

    13. ``artist_song_count``          — unique songs per artist
    14. ``artist_total_chart_days``    — unique chart days per artist
    15. ``artist_average_popularity``  — mean popularity per artist
    16. ``artist_dominance_index``     — ``artist_total_chart_days × artist_song_count``

    Parameters
    ----------
    df : pd.DataFrame
        The cleaned DataFrame produced by
        ``utils.preprocessing.preprocess_data()``.  Must contain the columns
        ``song``, ``artist``, ``date`` (datetime), ``popularity``, and
        ``position``.

    Returns
    -------
    pd.DataFrame
        A new DataFrame (the caller's original is **never** mutated) with all
        16 derived feature columns appended.  Row order may differ from the
        input due to the sort applied by ``_add_daily_rank_change_and_movement``;
        the integer index is reset before returning.

    Raises
    ------
    TypeError
        If *df* is not a :class:`pandas.DataFrame`.
    ValueError
        If *df* is empty, missing required columns, or ``date`` is not a
        datetime dtype.
    RuntimeError
        If an unexpected error occurs during any feature engineering step.

    Examples
    --------
    >>> from utils.loader import load_data
    >>> from utils.preprocessing import preprocess_data
    >>> from utils.feature_engineering import feature_engineering
    >>> df = feature_engineering(preprocess_data(load_data()))
    >>> "duration_minutes" in df.columns
    True
    >>> "artist_dominance_index" in df.columns
    True
    """
    try:
        _validate_input(df)

        # Work on an explicit copy — never mutate the caller's DataFrame.
        df = df.copy()

        # --- Song-level ---
        df = _add_duration_minutes(df)
        df = _add_song_chart_aggregates(df)
        df = _add_popularity_trend(df)
        df = _add_daily_rank_change_and_movement(df)  # sorts by (song, date)

        # --- Artist-level ---
        df = _add_artist_aggregates(df)

        df = df.reset_index(drop=True)

    except (TypeError, ValueError):
        raise
    except Exception as exc:
        raise RuntimeError(
            f"An unexpected error occurred during feature engineering: {exc}"
        ) from exc

    return df
