from fastapi import FastAPI
import pandas as pd
import random

app = FastAPI()

# This loads your 20,000 Odisha grid points into memory
df = pd.read_csv("data/ml_input_template.csv")

@app.get("/")
def home():
    return {"message": "OdiSafe Backend is LIVE and using Odisha Grid Data!"}

@app.get("/api/risk")
def get_risk(lat: float, lon: float):
    # Search for the closest grid point in your CSV
    match = df[(df['lat'].round(2) == round(lat, 2)) & (df['lon'].round(2) == round(lon, 2))]
    
    if not match.empty:
        result = match.iloc[0]
        return {
            "grid_id": str(result.get('grid_id')),
            "risk_level": str(result.get('risk_level')),
            "score": float(result.get('risk_score'))
        }
    return {"message": "Location outside Odisha", "risk_level": "Low", "score": 0.1}

@app.get("/api/map-data")
def get_map_data():
    # Sends 50 high-risk points for her to plot on the map
    sample = df.nlargest(50, 'risk_score')
    return sample[['lat', 'lon', 'risk_level']].to_dict(orient="records")

@app.post("/api/sos")
def post_sos(data: dict):
    return {"status": "SOS Received", "id": random.randint(1000, 9999)}