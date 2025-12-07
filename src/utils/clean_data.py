import pandas as pd

def load_openaq(path: str) -> pd.DataFrame:
    # Load CSV without date parsing
    df = pd.read_csv(path)

    # Normalize column names (lowercase everything)
    df.columns = df.columns.str.lower().str.strip()

    # After standardization, datetime columns will be:
    #   datetimelocal
    #   datetimeutc

    # Now safely parse normalized date column
    if "datetimelocal" in df.columns:
        df["timestamp"] = pd.to_datetime(df["datetimelocal"], errors="coerce")
    elif "datetime" in df.columns:
        df["timestamp"] = pd.to_datetime(df["datetime"], errors="coerce")
    else:
        raise ValueError("No valid datetime column found.")

    # Clean parameter names
    if "parameter" in df.columns:
        df["parameter"] = df["parameter"].str.lower().str.strip()

    # Keep only PM data
    df = df[df["parameter"].isin(["pm10", "pm25"])]

    # Sort for charts
    df = df.sort_values("timestamp")

    return df

