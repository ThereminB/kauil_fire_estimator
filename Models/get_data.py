import pandas as pd
import numpy as np
from datetime import datetime
import pickle

from sklearn.pipeline import Pipeline


def prepare_test_data(longitude, latitude, fire_date):
    """
    Prepare test data from geographical coordinates and date.
    """

    aggregated_data = pd.read_csv("Resources/aggregated_data.csv")

    # Define feature columns in the same order as training
    feature_columns = [
        "season_Winter",
        "season_Spring",
        "season_Summer",
        "season_Fall",
        "season_Winter_weather",
        "season_Spring_weather",
        "season_Summer_weather",
        "season_Fall_weather",
        "fire_intensity_index",
        "max_daily_area",
        "avg_daily_area",
        "extreme_growth_pct",
        "weather_severity_index",
        "max_fwi",
        "max_isi",
        "max_dmc",
        "max_tmax",
        "min_rh",
        "max_ws",
        "fuel_complexity_index",
        "avg_Biomass",
        "avg_Closure",
        "avg_prcC",
        "avg_dem",
        "avg_slope",
        "avg_twi",
        "avg_hydrodens10k",
    ]

    # Convert date to day of year
    date = datetime.strptime(fire_date, "%Y-%m-%d")
    dob = date.timetuple().tm_yday

    # Find the closest historical record
    aggregated_data["distance"] = np.sqrt(
        (aggregated_data["lon"] - float(longitude)) ** 2
        + (aggregated_data["lat"] - float(latitude)) ** 2
    )

    # Find the closest record
    similar_record = aggregated_data.loc[aggregated_data["distance"].idxmin()]

    print(similar_record)
    # Return the features needed for prediction
    return similar_record[feature_columns]


def predict_risk(test_data):
    with open("Resources/kauil_model.pkl", "rb") as file:
        pipeline = pickle.load(file)

    """Make predictions using the loaded pipeline."""
    # Ensure data is in correct format
    if isinstance(test_data, pd.Series):
        test_data = pd.DataFrame([test_data])

    # Make prediction using the pipeline
    risk_level = pipeline.predict(test_data)
    risk_probabilities = pipeline.predict_proba(test_data)

    return {
        "predicted_risk_level": risk_level[0],
        # "probability_distribution": {
        #     "Low": risk_probabilities[0][0],
        #     "Medium": risk_probabilities[0][1],
        #     "High": risk_probabilities[0][2],
        # },
        "confidence": max(risk_probabilities[0]),
    }
