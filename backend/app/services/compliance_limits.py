# Compliance Limit Database
LIMITS = {
    # AIR EMISSIONS
    "pm25": 60,
    "pm10": 100,
    "so2": 80,
    "nox": 80,
    "co": 2,
    "o3": 180,
    "nh3": 400,
    "benzene": 5,
    
    # WATER QUALITY
    "ph": (6.5, 8.5),
    "bod": 30,
    "cod": 250,
    "tss": 100,
    "tds": 2100,
    "oil_grease": 10,
    "ammonia": 50,
    "nitrate": 10,
    "phosphate": 5,
    
    # HEAVY METALS
    "lead": 0.1,
    "mercury": 0.01,
    "cadmium": 2.0,
    "chromium": 2.0,
    "arsenic": 0.2,
    "nickel": 5.0,
    
    # NOISE
    "day_noise": 75,
    "night_noise": 70,
}

RECOMMENDATIONS = {
    "pm25": "Install electrostatic precipitators",
    "pm10": "Improve dust suppression systems",
    "so2": "Install flue gas desulfurization",
    "nox": "Improve combustion efficiency",
    "co": "Improve process control",
    "ph": "Adjust neutralization process",
    "bod": "Upgrade wastewater treatment plant",
    "cod": "Improve effluent treatment process",
    "tss": "Install advanced filtration",
    "tds": "Implement reverse osmosis",
    "oil_grease": "Install oil-water separators",
    "ammonia": "Improve biological treatment",
    "nitrate": "Implement denitrification process",
    "phosphate": "Add chemical precipitation step",
    "lead": "Install heavy metal removal system",
    "mercury": "Install activated carbon filters",
    "cadmium": "Implement ion exchange process",
    "chromium": "Apply chemical reduction and precipitation",
    "arsenic": "Use adsorption or membrane filtration",
    "nickel": "Implement electrolytic recovery",
    "day_noise": "Install acoustic barriers",
    "night_noise": "Install acoustic barriers",
}
