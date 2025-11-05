from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import CarFeatures, PredictionResponse
import joblib
import pandas as pd
import os
from pathlib import Path

# Configuration - Compatible Docker et local
# En Docker: /app/ml/artifacts/model.joblib
# En local: ../../ml/artifacts/model.joblib
if os.path.exists("/app/ml/artifacts/model.joblib"):
    MODEL_PATH = Path("/app/ml/artifacts/model.joblib")
else:
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
print(f"[INFO] Tentative de chargement du modèle depuis: {MODEL_PATH}")
print(f"[INFO] Le fichier existe? {MODEL_PATH.exists()}")

if MODEL_PATH.exists():
    print(f"[INFO] Taille du fichier: {MODEL_PATH.stat().st_size} bytes")
    
try:
    model = joblib.load(MODEL_PATH)
    print(f"[SUCCESS] Modèle chargé avec succès: {MODEL_PATH}")
except FileNotFoundError:
    model = None
    print(f"[ERROR] Fichier modèle introuvable: {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"[ERROR] Erreur de chargement du modèle: {type(e).__name__}: {e}")

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
