"""
loader.py
---------
Data loading utilities for the Atlantic Music Analytics Streamlit app.
"""

import pandas as pd


DATA_PATH = "data/Atlantic_United_States.csv"


def load_data() -> pd.DataFrame:
    """Load and preprocess the Atlantic United States dataset.

    Reads the CSV file located at ``data/Atlantic_United_States.csv``,
    strips leading/trailing whitespace from all column names, and parses
    the ``date`` column into :class:`pandas.Timestamp` objects.

    Returns
    -------
    pd.DataFrame
        A cleaned DataFrame ready for downstream analysis.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist at the expected path.
    ValueError
        If the ``date`` column is missing or cannot be parsed as datetime.
    RuntimeError
        If the file exists but cannot be read or processed for any other reason.

    Examples
    --------
    >>> from utils.loader import load_data
    >>> df = load_data()
    >>> df.dtypes["date"]
    dtype('<M8[ns]')
    """
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Dataset not found at '{DATA_PATH}'. "
            "Please place 'Atlantic_United_States.csv' inside the 'data/' directory."
        ) from exc
    except Exception as exc:
        raise RuntimeError(
            f"Failed to read '{DATA_PATH}': {exc}"
        ) from exc

    # Strip leading/trailing whitespace from every column name.
    df.columns = df.columns.str.strip()
    
    # Map existing columns to what the app expects
    rename_mapping = {
        "track_name": "song",
        "release_date": "date",
    }
    df.rename(columns=rename_mapping, inplace=True)
    
    # Fill in missing required columns with dummy data if they don't exist
    if "position" not in df.columns:
        df["position"] = 1
    if "album_type" not in df.columns:
        df["album_type"] = "Album"
    if "is_explicit" not in df.columns:
        df["is_explicit"] = False
    if "total_tracks" not in df.columns:
        df["total_tracks"] = 12

    # Parse the 'date' column to datetime.
    if "date" not in df.columns:
        raise ValueError(
            "Expected a 'date' column in the dataset, but it was not found. "
            f"Available columns: {df.columns.tolist()}"
        )

    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception as exc:
        raise ValueError(
            f"Could not parse the 'date' column as datetime: {exc}"
        ) from exc

    return df
