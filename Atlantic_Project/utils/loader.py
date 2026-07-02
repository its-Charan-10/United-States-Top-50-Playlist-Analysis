from pathlib import Path
import pandas as pd

# Absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Atlantic_United_States.csv"


def load_data() -> pd.DataFrame:
    """Load Atlantic United States dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found.\nExpected location:\n{DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    return df
