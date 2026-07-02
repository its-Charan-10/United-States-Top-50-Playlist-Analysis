# Atlantic Music Analytics

A Streamlit-based dashboard for analyzing Atlantic music data across the United States.

## Project Structure

```
Atlantic_Project/
├── app.py                        # Main Streamlit entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── data/
│   └── Atlantic_United_States.csv  # Source dataset
├── pages/
│   ├── 1_Dashboard.py            # Overview & KPIs
│   ├── 2_Playlist_Analysis.py    # Playlist trends
│   ├── 3_Song_Analysis.py        # Song deep-dives
│   ├── 4_Artist_Analysis.py      # Artist statistics
│   ├── 5_Popularity.py           # Popularity trends
│   └── 6_Content_Analysis.py     # Content/lyrics analysis
├── utils/
│   ├── loader.py                 # Data loading utilities
│   ├── preprocessing.py          # Data cleaning & preprocessing
│   ├── feature_engineering.py    # Feature creation
│   └── charts.py                 # Reusable chart functions
└── assets/
    └── logo.png                  # Project logo
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Dataset

Place your dataset at `data/Atlantic_United_States.csv`.
