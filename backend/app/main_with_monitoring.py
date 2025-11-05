"""
Version de main.py avec monitoring intégré
Remplacez votre main.py actuel par ce fichier pour activer le monitoring
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import CarFeatures, PredictionResponse
from app.cache import cache
from app.monitoring import (
    MetricsMiddleware,
    metrics_endpoint,
    track_prediction,
    track_cache_hit,
    track_cache_miss,
    set_model_status,
    set_model_version
)
from app.prediction_tracker import tracker
import joblib
import pandas as pd
import os
from pathlib import Path
from time import time

# Configuration du modèle
if os.path.exists("/app/ml/artifacts/model.joblib"):
    MODEL_PATH = Path("/app/ml/artifacts/model.joblib")
else:
    MODEL_PATH = Path(__file__).parents[2] / "ml" / "artifacts" / "model.joblib"

app = FastAPI(
    title="CarPricePredictor-MA",
    description="API de prédiction du prix des voitures avec monitoring",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter le middleware de monitoring
app.middleware("http")(MetricsMiddleware(app))

# Charger le modèle
print(f"[INFO] Tentative de chargement du modèle depuis: {MODEL_PATH}")

try:
    model = joblib.load(MODEL_PATH)
    print(f"[SUCCESS] Modèle chargé avec succès")
    set_model_status(True)
    set_model_version("1.0.0", "2025-11-05")
except Exception as e:
    model = None
    print(f"[ERROR] Erreur de chargement du modèle: {e}")
    set_model_status(False)


@app.get("/")
def root():
    return {"message": "CarPricePredictor-MA API", "status": "running", "monitoring": "enabled"}


@app.get("/health")
def health():
    return {
        "status": "ok" if model else "error",
        "model_loaded": model is not None,
        "cache_enabled": cache.enabled
    }


@app.get("/metrics")
async def metrics():
    """Endpoint pour Prometheus"""
    from fastapi import Request
    return await metrics_endpoint(Request(scope={"type": "http"}))


@app.get("/cache/stats")
def cache_stats():
    """Statistiques du cache Redis"""
    return cache.get_stats()


@app.get("/predictions/stats")
def prediction_stats(date: str = None):
    """Statistiques des prédictions"""
    return tracker.get_stats(date)


@app.post("/predict", response_model=PredictionResponse)
def predict(features: CarFeatures):
    if model is None:
        track_prediction(0, success=False)
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    start_time = time()
    
    try:
        # Convertir en dict pour le cache
        car_data = features.model_dump()
        
        # Vérifier le cache
        cached_price = cache.get(car_data)
        
        if cached_price is not None:
            # Cache HIT
            track_cache_hit()
            response_time = (time() - start_time) * 1000
            
            # Logger la prédiction
            tracker.log_prediction(
                car_features=car_data,
                predicted_price=cached_price,
                cache_used=True,
                response_time_ms=response_time
            )
            
            # Tracker la métrique
            track_prediction(cached_price, success=True)
            
            return {"price_mad": round(cached_price, 2)}
        
        # Cache MISS - Faire la prédiction
        track_cache_miss()
        
        df = pd.DataFrame([car_data])
        price = float(model.predict(df)[0])
        
        # Mettre en cache
        cache.set(car_data, price, ttl=3600)
        
        response_time = (time() - start_time) * 1000
        
        # Logger la prédiction
        tracker.log_prediction(
            car_features=car_data,
            predicted_price=price,
            cache_used=False,
            response_time_ms=response_time
        )
        
        # Tracker la métrique
        track_prediction(price, success=True)
        
        return {"price_mad": round(price, 2)}
    
    except Exception as e:
        response_time = (time() - start_time) * 1000
        
        # Logger l'erreur
        tracker.log_prediction(
            car_features=car_data,
            predicted_price=0,
            cache_used=False,
            response_time_ms=response_time,
            status="error",
            error_message=str(e)
        )
        
        track_prediction(0, success=False)
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction: {str(e)}")
