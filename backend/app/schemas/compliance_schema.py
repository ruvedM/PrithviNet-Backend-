# Industry Compliance Schema
from pydantic import BaseModel, Field
from typing import Dict

class AirParams(BaseModel):
    pm25: float = 0
    pm10: float = 0
    so2: float = 0
    nox: float = 0
    co: float = 0
    o3: float = 0
    nh3: float = 0
    lead: float = 0
    benzene: float = 0

class WaterParams(BaseModel):
    ph: float = 0
    bod: float = 0
    cod: float = 0
    tss: float = 0
    tds: float = 0
    oil_grease: float = 0
    ammonia: float = 0
    nitrate: float = 0
    phosphate: float = 0

class HeavyMetalsParams(BaseModel):
    lead: float = 0
    mercury: float = 0
    cadmium: float = 0
    chromium: float = 0
    arsenic: float = 0
    nickel: float = 0

class NoiseParams(BaseModel):
    day_noise: float = 0
    night_noise: float = 0

class WasteParams(BaseModel):
    hazardous_waste_generated: float = 0
    hazardous_waste_disposed: float = 0
    solid_waste_generated: float = 0

class EmissionsParams(BaseModel):
    co2: float = 0
    methane: float = 0
    fuel_consumption: float = 0

class ComplianceReport(BaseModel):
    industry_name: str
    industry_type: str
    location: str
    air: AirParams
    water: WaterParams
    heavy_metals: HeavyMetalsParams
    noise: NoiseParams
    waste: WasteParams
    emissions: EmissionsParams
