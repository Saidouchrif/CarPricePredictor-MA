# ðŸš— CarPricePredictor-MA

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E.svg)](https://scikit-learn.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Application complÃ¨te de Machine Learning pour estimer le prix des voitures d'occasion au Maroc**

[ðŸŒ Demo Live](https://huggingface.co/spaces/SaidOuchrif/CarPricePredictor-MA) â€¢ [ðŸ“– GitHub](https://github.com/Saidouchrif/CarPricePredictor-MA) â€¢ [ðŸ¤— Hugging Face](https://huggingface.co/spaces/SaidOuchrif/CarPricePredictor-MA)

</div>

---

## ðŸ“‹ Table des MatiÃ¨res

- [Vue d'ensemble](#-vue-densemble)
- [Architecture du Projet](#ï¸-architecture-du-projet)
- [Structure des Dossiers](#-structure-des-dossiers)
- [Technologies UtilisÃ©es](#-technologies-utilisÃ©es)
- [FonctionnalitÃ©s](#-fonctionnalitÃ©s)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Monitoring](#-monitoring)
- [Tests](#-tests)
- [DÃ©ploiement](#-dÃ©ploiement)
- [Contributeur](#-contributeur)
- [Licence](#-licence)

---

## ðŸŽ¯ Vue d'ensemble

**CarPricePredictor-MA** est une application full-stack de Machine Learning qui permet d'estimer le prix rÃ©el d'une voiture d'occasion au Maroc Ã  partir de ses caractÃ©ristiques techniques et de son Ã©tat.

### ProblÃ©matique

Le marchÃ© des voitures d'occasion au Maroc manque de transparence dans la tarification. Les acheteurs ont du mal Ã  dÃ©terminer si le prix proposÃ© est juste.

### Solution

Une application web complÃ¨te avec:
- ðŸŽ¯ **Estimation prÃ©cise** basÃ©e sur Random Forest
- âš¡ **Performance optimale** avec cache Redis
- ðŸ“Š **Monitoring complet** Prometheus + Grafana
- ðŸ”’ **API REST** avec FastAPI
- ðŸ’» **Interface intuitive** Streamlit
- ðŸ³ **Docker ready**

---

## ðŸ—ï¸ Architecture du Projet

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚           PRESENTATION LAYER                â”‚
â”‚                                             â”‚
â”‚         Streamlit Frontend                  â”‚
â”‚           (Port 8501)                       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                  â”‚ HTTP REST
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          APPLICATION LAYER                  â”‚
â”‚                                             â”‚
â”‚          FastAPI Backend                    â”‚
â”‚            (Port 8000)                      â”‚
â”‚                                             â”‚
â”‚  /predict  â”‚  /health  â”‚  /metrics         â”‚
â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚            â”‚            â”‚
â”Œâ”€â”€â”€â”€â”´â”€â”€â”€â”   â”Œâ”€â”€â”€â”´â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”
â”‚ Redis  â”‚   â”‚   ML   â”‚   â”‚Prometheusâ”‚
â”‚ Cache  â”‚   â”‚ Model  â”‚   â”‚ Metrics  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜
                               â”‚
                          â”Œâ”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”
                          â”‚ Grafana  â”‚
                          â”‚Dashboard â”‚
                          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ“ Structure des Dossiers

```
CarPricePredictor-MA/
â”‚
â”œâ”€â”€ ðŸ“‚ backend/                      # Backend FastAPI
â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”œâ”€â”€ main.py                  # API principale
â”‚   â”‚   â”œâ”€â”€ schemas.py               # Validation Pydantic
â”‚   â”‚   â”œâ”€â”€ cache.py                 # Cache Redis
â”‚   â”‚   â”œâ”€â”€ monitoring.py            # MÃ©triques Prometheus
â”‚   â”‚   â””â”€â”€ prediction_tracker.py    # TraÃ§abilitÃ©
â”‚   â”œâ”€â”€ tests/                       # 27 tests unitaires
â”‚   â”‚   â”œâ”€â”€ test_main.py             # Tests API
â”‚   â”‚   â””â”€â”€ test_schemas.py          # Tests schÃ©mas
â”‚   â””â”€â”€ requirements.txt             # DÃ©pendances
â”‚
â”œâ”€â”€ ðŸ“‚ frontend/                     # Frontend Streamlit
â”‚   â”œâ”€â”€ app.py                       # Interface web
â”‚   â””â”€â”€ requirements.txt
â”‚
â”œâ”€â”€ ðŸ“‚ ml/                           # Machine Learning
â”‚   â””â”€â”€ artifacts/
â”‚       â””â”€â”€ model.joblib             # ModÃ¨le (50 MB)
â”‚
â”œâ”€â”€ ðŸ“‚ notebooks/                    # Jupyter Notebooks
â”‚   â”œâ”€â”€ CarPrice_ML.ipynb            # Pipeline ML complet
â”‚   â””â”€â”€ ReadData.ipynb               # Exploration donnÃ©es
â”‚
â”œâ”€â”€ ðŸ“‚ data/                         # DonnÃ©es
â”‚   â””â”€â”€ DataSet.csv                  # Dataset (898 KB)
â”‚
â”œâ”€â”€ ðŸ“‚ monitoring/                   # Monitoring
â”‚   â”œâ”€â”€ docker-compose.monitoring.yml
â”‚   â”œâ”€â”€ prometheus/
â”‚   â”‚   â”œâ”€â”€ prometheus.yml
â”‚   â”‚   â””â”€â”€ alerts.yml
â”‚   â””â”€â”€ grafana/
â”‚       â””â”€â”€ provisioning/
â”‚
â””â”€â”€ ðŸ³ Dockerfile                    # Hugging Face Spaces
```

---

## ðŸ› ï¸ Technologies UtilisÃ©es

### Backend
- **FastAPI 0.104.1** - Framework web moderne
- **Uvicorn** - Serveur ASGI
- **Pydantic** - Validation de donnÃ©es

### Frontend  
- **Streamlit 1.28.0** - Interface web ML

### Machine Learning
- **scikit-learn 1.6.1** - Framework ML
- **Pandas** - Manipulation de donnÃ©es
- **Joblib** - SÃ©rialisation modÃ¨le

### Monitoring
- **Redis 7.0** - Cache en mÃ©moire
- **Prometheus** - MÃ©triques
- **Grafana** - Visualisation

### DevOps
- **Docker** - Containerisation
- **Git LFS** - Gros fichiers
- **Pytest** - Tests unitaires

---

## âœ¨ FonctionnalitÃ©s

### ðŸŽ¯ PrÃ©diction de Prix
âœ… Estimation basÃ©e sur 13+ caractÃ©ristiques  
âœ… ModÃ¨le Random Forest optimisÃ©  
âœ… Validation temps rÃ©el  
âœ… Gestion des erreurs

### âš¡ Performance
âœ… Cache Redis (90% gain performance)  
âœ… Architecture async  
âœ… ModÃ¨le prÃ©-chargÃ© en mÃ©moire

### ðŸ“Š Monitoring
âœ… MÃ©triques Prometheus (requÃªtes, latence, erreurs)  
âœ… Dashboards Grafana  
âœ… Alertes automatiques  
âœ… Cache hit/miss rate

### ðŸ“ TraÃ§abilitÃ©
âœ… Logs JSON de toutes les prÃ©dictions  
âœ… ID unique par prÃ©diction  
âœ… Historique complet  
âœ… Versionnement modÃ¨le

### ðŸ§ª Tests
âœ… 27 tests unitaires (Pytest)  
âœ… Couverture 83%  
âœ… Tests endpoints API  
âœ… Tests validation schÃ©mas

---

## ðŸš€ Installation

### Option 1: Installation Locale

```bash
# Cloner le repo
git clone https://github.com/Saidouchrif/CarPricePredictor-MA.git
cd CarPricePredictor-MA

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (nouveau terminal)
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Docker

```bash
# Lancer avec Docker Compose
docker-compose up -d

# Services:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:8501
```

### Option 3: Avec Monitoring

```bash
# Lancer monitoring
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d

# Services:
# - Redis: localhost:6379
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin123)
```

---

## ðŸŽ¯ Utilisation

### Interface Web

1. Ouvrir http://localhost:8501
2. Remplir le formulaire
3. Cliquer "Estimer le prix (MAD)"
4. Obtenir le prix estimÃ©

### API REST

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Toyota",
    "model": "Corolla",
    "year": 2020,
    "fuel": "Petrol",
    "seller_type": "Individual",
    "transmission": "Manual",
    "km_driven": 25000.0,
    "engine_cc": 1600.0,
    "max_power_bhp": 120.0
  }'
```

**RÃ©ponse:**
```json
{
  "price_mad": 150000.50
}
```

---

## ðŸ“š API Documentation

### Endpoints

| Endpoint | MÃ©thode | Description |
|----------|---------|-------------|
| /predict | POST | PrÃ©dire le prix |
| /health | GET | Ã‰tat du systÃ¨me |
| /metrics | GET | MÃ©triques Prometheus |
| /cache/stats | GET | Stats cache Redis |
| /predictions/stats | GET | Stats prÃ©dictions |

### Documentation Interactive

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ðŸ“Š Monitoring

### MÃ©triques Prometheus

- http_requests_total - Total requÃªtes
- http_request_duration_seconds - Latence
- predictions_total - Total prÃ©dictions
- cache_hits_total - Cache hits
- cache_misses_total - Cache misses
- model_loaded - Statut modÃ¨le

### Grafana Dashboards

Ouvrir http://localhost:3000 (admin/admin123)

Dashboards disponibles:
- **API Performance** - Latence, throughput
- **ML Metrics** - PrÃ©dictions, prix
- **Cache Performance** - Hit rate
- **System Health** - CPU, RAM

---

## ðŸ§ª Tests

```bash
# Tous les tests
cd backend
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=app --cov-report=html

# RÃ©sultat: 27 tests passÃ©s, 83% couverture
```

### Tests inclus

- âœ… 17 tests endpoints API
- âœ… 10 tests schÃ©mas Pydantic
- âœ… Tests health check
- âœ… Tests prÃ©dictions
- âœ… Tests validation

---

## ðŸš€ DÃ©ploiement

### Hugging Face Spaces

Le projet est dÃ©ployÃ© sur:
ðŸŒ https://huggingface.co/spaces/SaidOuchrif/CarPricePredictor-MA

```bash
# DÃ©ployer
git push huggingface main

# Le build Docker prend ~5-10 minutes
```

### Docker Local

```bash
# Build
docker build -t carprice .

# Run
docker run -p 7860:7860 carprice
```

---

## ðŸ‘¨â€ðŸ’» Contributeur

<div align="center">

### Said Ouchrif

[![GitHub](https://img.shields.io/badge/GitHub-Saidouchrif-181717?logo=github)](https://github.com/Saidouchrif)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Said_Ouchrif-0A66C2?logo=linkedin)](https://linkedin.com/in/saidouchrif)
[![Hugging Face](https://img.shields.io/badge/ðŸ¤—_Hugging_Face-SaidOuchrif-FFD21E)](https://huggingface.co/SaidOuchrif)

**Data Scientist & ML Engineer**

PassionnÃ© par le Machine Learning et le dÃ©veloppement d'applications intelligentes.

</div>

---

## ðŸ“„ Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de dÃ©tails.

---

## ðŸ“ž Contact

- ðŸ“§ Email: contact@saidouchrif.com
- ðŸ™ GitHub: [@Saidouchrif](https://github.com/Saidouchrif)
- ðŸ¤— Hugging Face: [@SaidOuchrif](https://huggingface.co/SaidOuchrif)

---

## ðŸ™ Remerciements

- Dataset de voitures d'occasion au Maroc
- CommunautÃ© scikit-learn
- FastAPI et Streamlit
- Hugging Face pour l'hÃ©bergement

---

<div align="center">

**â­ Si ce projet vous aide, n'hÃ©sitez pas Ã  lui donner une Ã©toile! â­**

Made with â¤ï¸ by [Said Ouchrif](https://github.com/Saidouchrif)

</div>
