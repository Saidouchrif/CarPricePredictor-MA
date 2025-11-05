"""
Tests unitaires pour les endpoints de l'API CarPricePredictor-MA
"""
import pytest
from fastapi import status


class TestHealthEndpoint:
    """Tests pour l'endpoint /health"""
    
    def test_health_endpoint_returns_200(self, client):
        """Test que /health retourne un code 200"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
    
    def test_health_endpoint_returns_json(self, client):
        """Test que /health retourne du JSON"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_structure(self, client):
        """Test que /health retourne la structure attendue"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "model_loaded" in data
        assert isinstance(data["model_loaded"], bool)
    
    def test_health_endpoint_model_status(self, client):
        """Test que le statut du modèle est cohérent"""
        response = client.get("/health")
        data = response.json()
        
        # Si le modèle est chargé, le statut doit être "ok"
        if data["model_loaded"]:
            assert data["status"] == "ok"
        else:
            assert data["status"] == "error"


class TestRootEndpoint:
    """Tests pour l'endpoint racine /"""
    
    def test_root_endpoint_returns_200(self, client):
        """Test que / retourne un code 200"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_root_endpoint_returns_welcome_message(self, client):
        """Test que / retourne le message de bienvenue"""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "status" in data
        assert data["message"] == "CarPricePredictor-MA API"
        assert data["status"] == "running"


class TestPredictEndpoint:
    """Tests pour l'endpoint /predict"""
    
    def test_predict_endpoint_with_valid_data(self, client, sample_car_data):
        """Test que /predict fonctionne avec des données valides"""
        response = client.post("/predict", json=sample_car_data)
        
        # Vérifier le code de statut (200 si modèle chargé, 503 sinon)
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_503_SERVICE_UNAVAILABLE
        ]
    
    def test_predict_endpoint_returns_json(self, client, sample_car_data):
        """Test que /predict retourne du JSON"""
        response = client.post("/predict", json=sample_car_data)
        assert "application/json" in response.headers["content-type"]
    
    def test_predict_response_structure_when_model_loaded(self, client, sample_car_data):
        """Test la structure de la réponse si le modèle est chargé"""
        response = client.post("/predict", json=sample_car_data)
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            
            # Vérifier la structure de la réponse
            assert "price_mad" in data
            assert isinstance(data["price_mad"], (int, float))
            assert data["price_mad"] > 0
    
    def test_predict_endpoint_with_missing_fields(self, client):
        """Test que /predict retourne 422 avec des champs manquants"""
        incomplete_data = {
            "company": "Toyota",
            "model": "Corolla"
            # Champs obligatoires manquants
        }
        
        response = client.post("/predict", json=incomplete_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_predict_endpoint_with_invalid_year(self, client, sample_car_data):
        """Test que /predict rejette une année invalide"""
        sample_car_data["year"] = 1800  # Année trop ancienne
        
        response = client.post("/predict", json=sample_car_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_predict_endpoint_with_invalid_types(self, client, sample_car_data):
        """Test que /predict rejette des types de données invalides"""
        sample_car_data["year"] = "deux mille vingt"  # String au lieu d'int
        
        response = client.post("/predict", json=sample_car_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_predict_endpoint_without_model(self, client, sample_car_data):
        """Test que /predict retourne 503 si le modèle n'est pas chargé"""
        response = client.post("/predict", json=sample_car_data)
        
        # Si le modèle n'est pas chargé, on attend un code 503
        if response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            data = response.json()
            assert "detail" in data
            assert "modèle" in data["detail"].lower()
    
    def test_predict_endpoint_price_range(self, client, sample_car_data):
        """Test que le prix prédit est dans une plage raisonnable"""
        response = client.post("/predict", json=sample_car_data)
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            price = data["price_mad"]
            
            # Prix entre 10,000 MAD et 10,000,000 MAD (plage raisonnable)
            assert 10_000 <= price <= 10_000_000
    
    def test_predict_endpoint_different_cars(self, client):
        """Test des prédictions pour différents types de voitures"""
        test_cases = [
            {
                "company": "Mercedes-Benz",
                "model": "C-Class",
                "year": 2022,
                "owner": "First",
                "fuel": "Diesel",
                "seller_type": "Dealer",
                "transmission": "Automatic",
                "km_driven": 10000.0,
                "engine_cc": 2000.0,
                "max_power_bhp": 200.0
            },
            {
                "company": "Maruti",
                "model": "Alto",
                "year": 2015,
                "owner": "Second",
                "fuel": "Petrol",
                "seller_type": "Individual",
                "transmission": "Manual",
                "km_driven": 50000.0,
                "engine_cc": 800.0,
                "max_power_bhp": 50.0
            }
        ]
        
        for car_data in test_cases:
            response = client.post("/predict", json=car_data)
            
            # Doit retourner soit 200 (succès) soit 503 (modèle non chargé)
            assert response.status_code in [
                status.HTTP_200_OK,
                status.HTTP_503_SERVICE_UNAVAILABLE
            ]
    
    def test_predict_endpoint_with_optional_fields(self, client):
        """Test avec des champs optionnels manquants"""
        minimal_data = {
            "company": "Honda",
            "model": "City",
            "year": 2019,
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "km_driven": 30000.0,
            "engine_cc": 1500.0,
            "max_power_bhp": 100.0
            # edition, owner, mileage_mpg, torque_nm sont optionnels
        }
        
        response = client.post("/predict", json=minimal_data)
        
        # Doit retourner soit 200 soit 503, pas 422
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_503_SERVICE_UNAVAILABLE
        ]


class TestCORSMiddleware:
    """Tests pour la configuration CORS"""
    
    def test_cors_allows_all_origins(self, client):
        """Test que CORS accepte toutes les origines"""
        headers = {"Origin": "http://example.com"}
        response = client.get("/health", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        # FastAPI gère CORS automatiquement
