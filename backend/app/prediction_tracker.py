"""
Module de traçabilité des prédictions
Enregistre toutes les prédictions pour audit et analyse
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class PredictionLog:
    """Structure d'un log de prédiction"""
    timestamp: str
    prediction_id: str
    car_features: Dict[str, Any]
    predicted_price: float
    model_version: str
    cache_used: bool
    response_time_ms: float
    status: str  # 'success' ou 'error'
    error_message: Optional[str] = None


class PredictionTracker:
    """Tracker pour enregistrer toutes les prédictions"""
    
    def __init__(self, log_dir: str = "logs/predictions"):
        """
        Initialise le tracker
        
        Args:
            log_dir: Dossier pour stocker les logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.model_version = "1.0.0"  # À mettre à jour
        logger.info(f"📊 Prediction Tracker initialisé: {self.log_dir}")
    
    def _generate_prediction_id(self, car_features: Dict[str, Any]) -> str:
        """
        Génère un ID unique pour la prédiction
        
        Args:
            car_features: Caractéristiques de la voiture
            
        Returns:
            ID unique
        """
        timestamp = datetime.now().isoformat()
        data = f"{timestamp}:{json.dumps(car_features, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def log_prediction(
        self,
        car_features: Dict[str, Any],
        predicted_price: float,
        cache_used: bool,
        response_time_ms: float,
        status: str = "success",
        error_message: Optional[str] = None
    ):
        """
        Enregistre une prédiction
        
        Args:
            car_features: Caractéristiques de la voiture
            predicted_price: Prix prédit
            cache_used: True si provient du cache
            response_time_ms: Temps de réponse en ms
            status: Statut ('success' ou 'error')
            error_message: Message d'erreur si applicable
        """
        try:
            prediction_log = PredictionLog(
                timestamp=datetime.now().isoformat(),
                prediction_id=self._generate_prediction_id(car_features),
                car_features=car_features,
                predicted_price=predicted_price,
                model_version=self.model_version,
                cache_used=cache_used,
                response_time_ms=response_time_ms,
                status=status,
                error_message=error_message
            )
            
            # Écrire dans un fichier JSON par jour
            log_file = self._get_log_file()
            
            with open(log_file, 'a', encoding='utf-8') as f:
                json.dump(asdict(prediction_log), f, ensure_ascii=False)
                f.write('\n')
            
            logger.info(f"📝 Prédiction enregistrée: ID={prediction_log.prediction_id}")
        
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement de la prédiction: {e}")
    
    def _get_log_file(self) -> Path:
        """
        Retourne le fichier de log du jour
        
        Returns:
            Chemin vers le fichier de log
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return self.log_dir / f"predictions_{today}.jsonl"
    
    def get_stats(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Récupère les statistiques des prédictions
        
        Args:
            date: Date au format YYYY-MM-DD (défaut: aujourd'hui)
            
        Returns:
            Statistiques
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        log_file = self.log_dir / f"predictions_{date}.jsonl"
        
        if not log_file.exists():
            return {
                "date": date,
                "total_predictions": 0,
                "message": "Aucune prédiction pour cette date"
            }
        
        try:
            total = 0
            success = 0
            errors = 0
            cache_hits = 0
            prices = []
            response_times = []
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        log = json.loads(line)
                        total += 1
                        
                        if log["status"] == "success":
                            success += 1
                            prices.append(log["predicted_price"])
                        else:
                            errors += 1
                        
                        if log["cache_used"]:
                            cache_hits += 1
                        
                        response_times.append(log["response_time_ms"])
            
            return {
                "date": date,
                "total_predictions": total,
                "successful_predictions": success,
                "failed_predictions": errors,
                "cache_hits": cache_hits,
                "cache_hit_rate": round((cache_hits / total) * 100, 2) if total > 0 else 0,
                "average_price": round(sum(prices) / len(prices), 2) if prices else 0,
                "min_price": min(prices) if prices else 0,
                "max_price": max(prices) if prices else 0,
                "average_response_time_ms": round(sum(response_times) / len(response_times), 2) if response_times else 0
            }
        
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return {
                "date": date,
                "error": str(e)
            }
    
    def set_model_version(self, version: str):
        """
        Met à jour la version du modèle
        
        Args:
            version: Nouvelle version
        """
        self.model_version = version
        logger.info(f"🔄 Version du modèle mise à jour: {version}")


# Instance globale du tracker
tracker = PredictionTracker()
