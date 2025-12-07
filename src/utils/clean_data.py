import pandas as pd

def load_openaq(path: str) -> pd.DataFrame:
    # Load CSV using the correct date column
    df = pd.read_csv(path, parse_dates=["datetimeLocal"])

    # Standardize to a timestamp column for the app
    df["timestamp"] = df["datetimeLocal"]

    # Clean parameter names
    df["parameter"] = df["parameter"].str.lower().str.strip()

    # Keep only pm25 + pm10 for now
    df = df[df["parameter"].isin(["pm25", "pm10"])]

    # Sort for charts
    df = df.sort_values("timestamp")

    return df

