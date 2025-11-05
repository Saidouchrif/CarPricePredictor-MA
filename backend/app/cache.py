"""
Module de gestion du cache Redis pour les prédictions
"""
import redis
import json
import hashlib
from typing import Optional, Dict, Any
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class RedisCache:
    """Gestionnaire de cache Redis pour les prédictions"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """
        Initialise la connexion Redis
        
        Args:
            host: Hôte Redis
            port: Port Redis
            db: Numéro de base de données Redis
        """
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            # Test de connexion
            self.client.ping()
            self.enabled = True
            logger.info(f"✅ Redis connecté: {host}:{port}")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            self.enabled = False
            logger.warning(f"⚠️ Redis non disponible: {e}. Cache désactivé.")
    
    def _generate_key(self, car_features: Dict[str, Any]) -> str:
        """
        Génère une clé unique pour les features d'une voiture
        
        Args:
            car_features: Caractéristiques de la voiture
            
        Returns:
            Clé de cache unique
        """
        # Trier les clés pour avoir un hash cohérent
        sorted_features = json.dumps(car_features, sort_keys=True)
        hash_object = hashlib.md5(sorted_features.encode())
        return f"prediction:{hash_object.hexdigest()}"
    
    def get(self, car_features: Dict[str, Any]) -> Optional[float]:
        """
        Récupère une prédiction depuis le cache
        
        Args:
            car_features: Caractéristiques de la voiture
            
        Returns:
            Prix prédit ou None si non trouvé
        """
        if not self.enabled:
            return None
        
        try:
            key = self._generate_key(car_features)
            cached_value = self.client.get(key)
            
            if cached_value:
                logger.info(f"✅ Cache HIT: {key[:20]}...")
                return float(cached_value)
            else:
                logger.info(f"❌ Cache MISS: {key[:20]}...")
                return None
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du cache: {e}")
            return None
    
    def set(
        self,
        car_features: Dict[str, Any],
        price: float,
        ttl: int = 3600
    ) -> bool:
        """
        Stocke une prédiction dans le cache
        
        Args:
            car_features: Caractéristiques de la voiture
            price: Prix prédit
            ttl: Durée de vie en secondes (défaut: 1 heure)
            
        Returns:
            True si succès, False sinon
        """
        if not self.enabled:
            return False
        
        try:
            key = self._generate_key(car_features)
            self.client.setex(
                name=key,
                time=timedelta(seconds=ttl),
                value=str(price)
            )
            logger.info(f"💾 Prédiction mise en cache: {key[:20]}... = {price:.2f}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture du cache: {e}")
            return False
    
    def clear_all(self) -> int:
        """
        Efface toutes les prédictions en cache
        
        Returns:
            Nombre de clés supprimées
        """
        if not self.enabled:
            return 0
        
        try:
            keys = self.client.keys("prediction:*")
            if keys:
                deleted = self.client.delete(*keys)
                logger.info(f"🗑️ {deleted} prédictions supprimées du cache")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage du cache: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques du cache
        
        Returns:
            Dictionnaire avec les stats Redis
        """
        if not self.enabled:
            return {"enabled": False}
        
        try:
            info = self.client.info()
            prediction_keys = len(self.client.keys("prediction:*"))
            
            return {
                "enabled": True,
                "total_predictions_cached": prediction_keys,
                "memory_used_mb": info.get("used_memory", 0) / (1024 * 1024),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(info)
            }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return {"enabled": False, "error": str(e)}
    
    def _calculate_hit_rate(self, info: Dict) -> float:
        """Calcule le taux de succès du cache"""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return round((hits / total) * 100, 2)
    
    def close(self):
        """Ferme la connexion Redis"""
        if self.enabled:
            try:
                self.client.close()
                logger.info("🔒 Connexion Redis fermée")
            except Exception as e:
                logger.error(f"Erreur lors de la fermeture Redis: {e}")


# Instance globale du cache
cache = RedisCache()
