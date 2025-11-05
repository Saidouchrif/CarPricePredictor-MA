from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import CarFeatures, PredictionResponse
import joblib
import pandas as pd
from pathlib import Path

# Configuration
MODEL_PATH = Path(__file__).parents[2] / "ml" / "artifacts" / "model.joblib"

app = FastAPI(
    title="CarPricePredictor-MA",
    description="API de prédiction du prix des voitures",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle
try:
    model = joblib.load(MODEL_PATH)
    print(f" Modèle chargé: {MODEL_PATH}")
except Exception as e:
    model = None
    print(f" Erreur de chargement: {e}")

@app.get("/")
def root():
    return {"message": "CarPricePredictor-MA API", "status": "running"}

@app.get("/health")
def health():
    return {
        "status": "ok" if model else "error",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(features: CarFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    try:
        # Convertir en DataFrame
        df = pd.DataFrame([features.model_dump()])
        
        # Prédiction
        price = float(model.predict(df)[0])
        
        return {"price_mad": round(price, 2)}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction: {str(e)}")
