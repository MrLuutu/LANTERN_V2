import pandas as pd

def clean_data(df):
    #remove unused values
    clean_df = df[["parameter", "value", "unit", "datetimeLocal"]].copy()

    #drop N/A values. Drop 0 values
    clean_df.dropna(subset=["value"], inplace=True)
    clean_df = clean_df[clean_df["value"] != 0]

    #Make sure all parameters are uppercase and properly titled
    clean_df["parameter"] = clean_df["parameter"].str.upper()
    clean_df["parameter"] = clean_df["parameter"].replace({"P25": "PM2.5",
                                                           "PM1": "PM10",
                                                           "RELATIVEHUMIDITY": "Humidity",
                                                           "TEMPERATURE": "Temperature",
                                                           "UM003": "Ultrafine Particles"})

    return clean_df