from fastapi import APIRouter
from pydantic import BaseModel
from app.services.environment_service import (
    predict_air,
    predict_noise,
    predict_water
)


router = APIRouter(
    prefix="/environment",
    tags=["Environment Prediction"]
)


# -----------------------------
# REQUEST SCHEMAS
# -----------------------------

class AirData(BaseModel):
    PM2_5: float
    PM10: float
    NO: float
    NO2: float
    NOx: float
    NH3: float
    CO: float
    SO2: float
    O3: float
    Benzene: float
    Toluene: float
    Xylene: float

class NoiseData(BaseModel):
    traffic_density: float
    vehicle_count: float
    honking_events: float
    population_density: float
    near_highway: float
    near_construction: float
    industrial_zone: float


class WaterData(BaseModel):
    Temp: float
    DO: float
    pH: float
    BOD: float
    Nitrate: float
    Conductivity: float
    Fecal: float
    TotalColiform: float


# -----------------------------
# ROUTES
# -----------------------------

@router.post("/predict-air")
def air_prediction(data: AirData):

    result = predict_air(data.dict())

    return {
        "status": "success",
        "data": result
    }


@router.post("/predict-noise")
def noise_prediction(data: NoiseData):

    result = predict_noise(data.dict())

    return {
        "status": "success",
        "data": result
    }


@router.post("/predict-water")
def water_prediction(data: WaterData):
    return predict_water(data.dict())