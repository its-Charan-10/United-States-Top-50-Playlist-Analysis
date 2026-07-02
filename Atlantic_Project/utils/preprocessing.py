"""
preprocessing.py
----------------
Data preprocessing utilities for the Atlantic Music Analytics Streamlit app.

This module provides a single public entry-point, ``preprocess_data()``, which
applies a deterministic cleaning pipeline to the raw DataFrame returned by
``utils.loader.load_data()``.  Every step is isolated into a private helper so
that individual transformations are easy to test and extend independently.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Columns that must be present in the raw DataFrame.
REQUIRED_COLUMNS: list[str] = [
    "song",
    "artist",
    "date",
    "popularity",
    "position",
]

#: Columns that must be coerced to a numeric dtype.
NUMERIC_COLUMNS: list[str] = ["popularity", "duration_ms", "total_tracks"]

#: Valid inclusive range for playlist position.
POSITION_MIN: int = 1
POSITION_MAX: int = 50


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _validate_input(df: pd.DataFrame) -> None:
    """Raise ``TypeError`` or ``ValueError`` for obviously invalid input.

    Parameters
    ----------
    df:
        The raw DataFrame to validate.

    Raises
    ------
    TypeError
        If *df* is not a :class:`pandas.DataFrame`.
    ValueError
        If *df* is empty, or if any column listed in :data:`REQUIRED_COLUMNS`
        is absent.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"Expected a pandas DataFrame, got {type(df).__name__!r}."
        )
    if df.empty:
        raise ValueError("The input DataFrame is empty — nothing to preprocess.")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"The following required columns are missing from the dataset: "
            f"{missing}.  Available columns: {df.columns.tolist()}"
        )


def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully duplicate rows, then drop duplicates on (date, song).

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with duplicates removed; original row order is preserved.
    """
    before = len(df)
    df = df.drop_duplicates()
    full_dupes = before - len(df)

    df = df.drop_duplicates(subset=["date", "song"], keep="first")
    pair_dupes = before - full_dupes - len(df)

    if full_dupes or pair_dupes:
        print(
            f"[preprocessing] Removed {full_dupes} fully duplicate row(s) "
            f"and {pair_dupes} (date, song) duplicate(s)."
        )
    return df


def _drop_missing_critical(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows where any critical column contains a null value.

    Critical columns: ``song``, ``artist``, ``date``, ``popularity``,
    ``position``.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with incomplete rows removed.
    """
    before = len(df)
    df = df.dropna(subset=REQUIRED_COLUMNS)
    dropped = before - len(df)
    if dropped:
        print(f"[preprocessing] Dropped {dropped} row(s) with missing critical values.")
    return df


def _validate_position(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where ``position`` is outside [{POSITION_MIN}, {POSITION_MAX}].

    Parameters
    ----------
    df:
        Input DataFrame (``position`` must already be present).

    Returns
    -------
    pd.DataFrame
        DataFrame containing only rows with a valid playlist position.
    """
    before = len(df)
    mask = df["position"].between(POSITION_MIN, POSITION_MAX)
    df = df.loc[mask]
    dropped = before - len(df)
    if dropped:
        print(
            f"[preprocessing] Removed {dropped} row(s) with position "
            f"outside [{POSITION_MIN}, {POSITION_MAX}]."
        )
    return df


def _strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from ``song`` and ``artist`` columns.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with whitespace-stripped string columns.
    """
    for col in ("song", "artist"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df


def _normalise_text_case(df: pd.DataFrame) -> pd.DataFrame:
    """Convert ``artist`` and ``album_type`` columns to title case.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with normalised text casing.
    """
    for col in ("artist", "album_type"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()
    return df


def _convert_is_explicit(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce ``is_explicit`` to :class:`bool`.

    Handles common string representations (``"True"`` / ``"False"``,
    ``"1"`` / ``"0"``, ``"yes"`` / ``"no"``) in addition to native
    numeric or boolean values.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame where ``is_explicit`` is a boolean column.
    """
    if "is_explicit" not in df.columns:
        return df

    truthy = {"true", "1", "yes", "y", "t"}
    col = df["is_explicit"]

    if pd.api.types.is_bool_dtype(col):
        return df

    df["is_explicit"] = (
        col.astype(str).str.strip().str.lower().isin(truthy)
    )
    return df


def _coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce :data:`NUMERIC_COLUMNS` to a numeric dtype.

    Non-parseable values are set to ``NaN``.  Only columns that are
    actually present in *df* are processed.

    Parameters
    ----------
    df:
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with numeric columns properly typed.
    """
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _remove_invalid_numeric_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with a negative ``duration_ms`` or non-positive ``total_tracks``.

    Parameters
    ----------
    df:
        Input DataFrame (*must* have been through :func:`_coerce_numeric_columns`
        first so that the columns carry a numeric dtype).

    Returns
    -------
    pd.DataFrame
        DataFrame with physically invalid rows removed.
    """
    before = len(df)

    if "duration_ms" in df.columns:
        df = df.loc[~(df["duration_ms"] < 0)]

    if "total_tracks" in df.columns:
        df = df.loc[~(df["total_tracks"] <= 0)]

    dropped = before - len(df)
    if dropped:
        print(
            f"[preprocessing] Removed {dropped} row(s) with invalid "
            "duration_ms or total_tracks values."
        )
    return df


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the full cleaning pipeline to the raw Atlantic music DataFrame.

    The pipeline executes the following steps in order:

    1. Input validation — raises if *df* is wrong type, empty, or missing
       required columns.
    2. Remove fully duplicate rows and (date, song) duplicates.
    3. Drop rows where ``song``, ``artist``, ``date``, ``popularity``, or
       ``position`` are null.
    4. Validate and filter playlist ``position`` to [1, 50].
    5. Strip whitespace from ``song`` and ``artist`` values.
    6. Title-case ``artist`` and ``album_type`` values.
    7. Coerce ``is_explicit`` to :class:`bool`.
    8. Coerce ``popularity``, ``duration_ms``, and ``total_tracks`` to numeric.
    9. Remove rows with negative ``duration_ms`` or ``total_tracks`` ≤ 0.
    10. Reset the DataFrame index.

    Parameters
    ----------
    df:
        The raw :class:`pandas.DataFrame` returned by ``utils.loader.load_data()``.

    Returns
    -------
    pd.DataFrame
        A fully cleaned DataFrame with a freshly reset integer index.

    Raises
    ------
    TypeError
        If *df* is not a :class:`pandas.DataFrame`.
    ValueError
        If *df* is empty or missing required columns.
    RuntimeError
        If an unexpected error occurs during any preprocessing step.

    Examples
    --------
    >>> from utils.loader import load_data
    >>> from utils.preprocessing import preprocess_data
    >>> raw_df = load_data()
    >>> clean_df = preprocess_data(raw_df)
    >>> clean_df.index[0]
    0
    """
    try:
        _validate_input(df)

        # Work on an explicit copy so the caller's DataFrame is never mutated.
        df = df.copy()

        df = _remove_duplicates(df)
        df = _drop_missing_critical(df)
        df = _validate_position(df)
        df = _strip_string_columns(df)
        df = _normalise_text_case(df)
        df = _convert_is_explicit(df)
        df = _coerce_numeric_columns(df)
        df = _remove_invalid_numeric_rows(df)

        df = df.reset_index(drop=True)

    except (TypeError, ValueError):
        # Re-raise validation errors unchanged so callers can inspect them.
        raise
    except Exception as exc:
        raise RuntimeError(
            f"An unexpected error occurred during preprocessing: {exc}"
        ) from exc

    return df
