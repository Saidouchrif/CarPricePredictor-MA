"""
Tests unitaires pour les schémas Pydantic
"""
import pytest
from pydantic import ValidationError
from app.schemas import CarFeatures, PredictionResponse


class TestCarFeaturesSchema:
    """Tests pour le schéma CarFeatures"""
    
    def test_valid_car_features(self):
        """Test la création d'un CarFeatures valide"""
        data = {
            "company": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "km_driven": 25000.0,
            "engine_cc": 1600.0,
            "max_power_bhp": 120.0
        }
        
        car = CarFeatures(**data)
        assert car.company == "Toyota"
        assert car.year == 2020
        assert car.km_driven == 25000.0
    
    def test_car_features_with_optional_fields(self):
        """Test avec les champs optionnels"""
        data = {
            "company": "Honda",
            "model": "City",
            "edition": "VX",
            "year": 2019,
            "owner": "First",
            "fuel": "Diesel",
            "seller_type": "Dealer",
            "transmission": "Automatic",
            "km_driven": 15000.0,
            "mileage_mpg": 20.5,
            "engine_cc": 1500.0,
            "max_power_bhp": 100.0,
            "torque_nm": 200.0
        }
        
        car = CarFeatures(**data)
        assert car.edition == "VX"
        assert car.owner == "First"
        assert car.mileage_mpg == 20.5
        assert car.torque_nm == 200.0
    
    def test_car_features_year_validation_min(self):
        """Test que l'année doit être >= 1990"""
        data = {
            "company": "Toyota",
            "model": "Corolla",
            "year": 1989,  # Trop ancien
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "km_driven": 25000.0,
            "engine_cc": 1600.0,
            "max_power_bhp": 120.0
        }
        
        with pytest.raises(ValidationError) as exc_info:
            CarFeatures(**data)
        
        assert "year" in str(exc_info.value)
    
    def test_car_features_year_validation_max(self):
        """Test que l'année doit être <= 2026"""
        data = {
            "company": "Toyota",
            "model": "Corolla",
            "year": 2027,  # Trop récent
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "km_driven": 25000.0,
            "engine_cc": 1600.0,
            "max_power_bhp": 120.0
        }
        
        with pytest.raises(ValidationError) as exc_info:
            CarFeatures(**data)
        
        assert "year" in str(exc_info.value)
    
    def test_car_features_missing_required_fields(self):
        """Test qu'une erreur est levée si des champs requis manquent"""
        data = {
            "company": "Toyota",
            "model": "Corolla"
            # Champs obligatoires manquants
        }
        
        with pytest.raises(ValidationError):
            CarFeatures(**data)
    
    def test_car_features_invalid_types(self):
        """Test que les types de données sont validés"""
        data = {
            "company": "Toyota",
            "model": "Corolla",
            "year": "deux mille vingt",  # String au lieu d'int
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "km_driven": 25000.0,
            "engine_cc": 1600.0,
            "max_power_bhp": 120.0
        }
        
        with pytest.raises(ValidationError):
            CarFeatures(**data)


class TestPredictionResponseSchema:
    """Tests pour le schéma PredictionResponse"""
    
    def test_valid_prediction_response(self):
        """Test la création d'une réponse de prédiction valide"""
        response = PredictionResponse(price_mad=150000.50)
        
        assert response.price_mad == 150000.50
        assert isinstance(response.price_mad, float)
    
    def test_prediction_response_as_dict(self):
        """Test la conversion en dictionnaire"""
        response = PredictionResponse(price_mad=200000.0)
        data = response.model_dump()
        
        assert "price_mad" in data
        assert data["price_mad"] == 200000.0
    
    def test_prediction_response_missing_field(self):
        """Test qu'une erreur est levée si price_mad manque"""
        with pytest.raises(ValidationError):
            PredictionResponse()
    
    def test_prediction_response_invalid_type(self):
        """Test que price_mad doit être numérique"""
        with pytest.raises(ValidationError):
            PredictionResponse(price_mad="cent mille")
