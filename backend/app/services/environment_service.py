import os
import joblib
import pandas as pd


# Get base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model paths
AIR_MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "air_model.pkl")
NOISE_MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "noise_model.pkl")
WATER_MODEL_PATH = os.path.join(BASE_DIR, "ai_models", "water_model.pkl")


# Load models once when server starts
air_model = joblib.load(AIR_MODEL_PATH)
noise_model = joblib.load(NOISE_MODEL_PATH)
water_model = joblib.load(WATER_MODEL_PATH)


# -----------------------------
# AIR POLLUTION PREDICTION
# -----------------------------
def predict_air(data: dict):

    df = pd.DataFrame([data])

    prediction = air_model.predict(df)

    return {
        "pollution_type": "air",
        "prediction": float(prediction[0])
    }


# -----------------------------
# NOISE POLLUTION PREDICTION
# -----------------------------
def predict_noise(data: dict):
    try:
        import pandas as pd

        # Expected feature order for model
        columns = [
            "traffic_density",
            "vehicle_count",
            "honking_events",
            "population_density",
            "near_highway",
            "near_construction",
            "industrial_zone"
        ]

        # Convert request to DataFrame
        df = pd.DataFrame([[data.get(col, 0) for col in columns]], columns=columns)

        # Model prediction
        prediction = noise_model.predict(df)

        return {
            "pollution_type": "noise",
            "prediction": prediction[0]
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# -----------------------------
# WATER POLLUTION PREDICTION
# -----------------------------
def predict_water(data: dict):
    try:

        # EXACT order used during training
        columns = [
            "Temp",
            "DO",
            "pH",
            "Conductivity",
            "BOD",
            "Nitrate",
            "Fecal",
            "TotalColiform"
        ]

        # Default temperature if not provided
        if "Temp" not in data:
            data["Temp"] = 25

        # Create dataframe in exact order
        df = pd.DataFrame([[data.get(col, 0) for col in columns]], columns=columns)

        prediction = water_model.predict(df)

        return {
            "status": "success",
            "data": {
                "pollution_type": "water",
                "prediction": prediction[0]
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }