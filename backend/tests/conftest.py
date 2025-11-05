"""
Configuration des fixtures Pytest pour les tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Fixture qui retourne un client de test FastAPI"""
    return TestClient(app)

@pytest.fixture
def sample_car_data():
    """Fixture avec des données de voiture valides pour les tests"""
    return {
        "company": "Toyota",
        "model": "Corolla",
        "edition": "GLi",
        "year": 2020,
        "owner": "First",
        "fuel": "Petrol",
        "seller_type": "Individual",
        "transmission": "Manual",
        "km_driven": 25000.0,
        "mileage_mpg": 18.5,
        "engine_cc": 1600.0,
        "max_power_bhp": 120.0,
        "torque_nm": 150.0
    }

@pytest.fixture
def invalid_car_data():
    """Fixture avec des données invalides pour tester la validation"""
    return {
        "company": "Toyota",
        "model": "Corolla",
        "year": 1800,  # Année invalide
        "owner": "First",
        "fuel": "Petrol",
        "seller_type": "Individual",
        "transmission": "Manual",
        "km_driven": -5000.0,  # Kilométrage négatif
        "engine_cc": 1600.0,
        "max_power_bhp": 120.0
    }
