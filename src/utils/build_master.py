import pandas as pd

def load_city(path, city_name):
    df = pd.read_csv(path)
    df["city"] = city_name
    # Normalize datetime column
    df["datetime"] = pd.to_datetime(df["datetimelocal"])
    return df[[
        "city", "location_id", "location_name", "parameter",
        "value", "unit", "datetime", "latitude", "longitude"
    ]]

def build_master():
    kampala = load_city("data/clean_openaq.csv", "Kampala")
    boston = load_city("data/openaq_boston.csv", "Boston")

    master = pd.concat([kampala, boston], ignore_index=True)
    master.to_csv("data/air_quality_master.csv", index=False)
    print("Master dataset created: data/air_quality_master.csv")

if __name__ == "__main__":
    build_master()
