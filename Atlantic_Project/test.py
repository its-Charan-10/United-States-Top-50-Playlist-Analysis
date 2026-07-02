import traceback
try:
    from utils.loader import load_data
    from utils.preprocessing import preprocess_data
    from utils.feature_engineering import feature_engineering
    raw = load_data()
    clean = preprocess_data(raw)
    enriched = feature_engineering(clean)
    print('Success!')
except Exception as e:
    traceback.print_exc()
