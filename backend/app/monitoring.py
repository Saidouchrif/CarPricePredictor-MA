"""
Module de monitoring avec Prometheus pour FastAPI
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from time import time
import logging

logger = logging.getLogger(__name__)

# === Métriques Prometheus ===

# Compteur de requêtes HTTP
http_requests_total = Counter(
    'http_requests_total',
    'Total des requêtes HTTP',
    ['method', 'endpoint', 'status']
)

# Histogramme de latence
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'Durée des requêtes HTTP en secondes',
    ['method', 'endpoint']
)

# Compteur de prédictions
predictions_total = Counter(
    'predictions_total',
    'Total des prédictions effectuées',
    ['status']  # 'success' ou 'error'
)

# Histogramme des prix prédits
predicted_prices = Histogram(
    'predicted_prices_mad',
    'Distribution des prix prédits en MAD',
    buckets=[10000, 50000, 100000, 200000, 500000, 1000000, 5000000, 10000000]
)

# Gauge pour le statut du modèle
model_loaded = Gauge(
    'model_loaded',
    'Statut du modèle ML (1=chargé, 0=non chargé)'
)

# Compteur de cache
cache_hits_total = Counter(
    'cache_hits_total',
    'Total des hits du cache Redis'
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total des misses du cache Redis'
)

# Gauge pour les stats du cache
cache_size = Gauge(
    'cache_size_predictions',
    'Nombre de prédictions en cache'
)

# Compteur de versions du modèle
model_version_info = Gauge(
    'model_version_info',
    'Information sur la version du modèle',
    ['version', 'trained_date']
)


class MetricsMiddleware:
    """Middleware pour collecter les métriques Prometheus"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Capturer le début de la requête
        start_time = time()
        
        # Créer un wrapper pour capturer le status code
        status_code = 500
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Enregistrer les métriques
            duration = time() - start_time
            method = scope["method"]
            path = scope["path"]
            
            # Ignorer l'endpoint /metrics lui-même
            if path != "/metrics":
                http_requests_total.labels(
                    method=method,
                    endpoint=path,
                    status=status_code
                ).inc()
                
                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=path
                ).observe(duration)


def track_prediction(price: float, success: bool = True):
    """
    Enregistre une prédiction dans les métriques
    
    Args:
        price: Prix prédit
        success: True si la prédiction a réussi
    """
    status = "success" if success else "error"
    predictions_total.labels(status=status).inc()
    
    if success and price > 0:
        predicted_prices.observe(price)


def track_cache_hit():
    """Enregistre un hit du cache"""
    cache_hits_total.inc()


def track_cache_miss():
    """Enregistre un miss du cache"""
    cache_misses_total.inc()


def set_model_status(loaded: bool):
    """
    Met à jour le statut du modèle
    
    Args:
        loaded: True si le modèle est chargé
    """
    model_loaded.set(1 if loaded else 0)


def set_model_version(version: str, trained_date: str):
    """
    Enregistre la version du modèle
    
    Args:
        version: Version du modèle
        trained_date: Date d'entraînement
    """
    model_version_info.labels(
        version=version,
        trained_date=trained_date
    ).set(1)


def update_cache_size(size: int):
    """
    Met à jour la taille du cache
    
    Args:
        size: Nombre de prédictions en cache
    """
    cache_size.set(size)


async def metrics_endpoint(request: Request) -> Response:
    """
    Endpoint pour exposer les métriques Prometheus
    
    Returns:
        Métriques au format Prometheus
    """
    metrics_data = generate_latest()
    return Response(
        content=metrics_data,
        media_type=CONTENT_TYPE_LATEST
    )
