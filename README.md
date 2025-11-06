# 🚗 CarPricePredictor-MA

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E.svg)](https://scikit-learn.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[![CI/CD Pipeline](https://github.com/Saidouchrif/CarPricePredictor-MA/actions/workflows/ci.yml/badge.svg)](https://github.com/Saidouchrif/CarPricePredictor-MA/actions/workflows/ci.yml)
[![Test Coverage](https://github.com/Saidouchrif/CarPricePredictor-MA/actions/workflows/test-coverage.yml/badge.svg)](https://github.com/Saidouchrif/CarPricePredictor-MA/actions/workflows/test-coverage.yml)
[![codecov](https://codecov.io/gh/Saidouchrif/CarPricePredictor-MA/branch/main/graph/badge.svg)](https://codecov.io/gh/Saidouchrif/CarPricePredictor-MA)

**Application complète de Machine Learning pour estimer le prix des voitures d'occasion au Maroc**

[🌐 Demo Live](https://huggingface.co/spaces/SaidOuchrif/CarPricePredictor-MA) • [📖 GitHub](https://github.com/Saidouchrif/CarPricePredictor-MA) • [🤗 Hugging Face](https://huggingface.co/spaces/SaidOuchrif/CarPricePredictor-MA)

</div>

---

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture du Projet](#️-architecture-du-projet)
- [Structure des Dossiers](#-structure-des-dossiers)
- [Technologies Utilisées](#-technologies-utilisées)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Monitoring](#-monitoring)
- [Tests](#-tests)
- [Déploiement](#-déploiement)
- [Contributeur](#-contributeur)
- [Licence](#-licence)

---

## 🎯 Vue d'ensemble

**CarPricePredictor-MA** est une application full-stack de Machine Learning qui permet d'estimer le prix réel d'une voiture d'occasion au Maroc à partir de ses caractéristiques techniques et de son état.

### Problématique

Le marché des voitures d'occasion au Maroc manque de transparence dans la tarification. Les acheteurs ont du mal à déterminer si le prix proposé est juste.

### Solution

Une application web complète avec:
- 🎯 **Estimation précise** basée sur Random Forest
- ⚡ **Performance optimale** avec cache Redis
- 📊 **Monitoring complet** Prometheus + Grafana
- 🔒 **API REST** avec FastAPI
- 💻 **Interface intuitive** Streamlit
- 🐳 **Docker ready**

---

## 🏗️ Architecture du Projet

### 📐 Architecture Globale en Couches

```
┌─────────────────────────────────────────────────────────────────┐
│                    COUCHE PRÉSENTATION                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Streamlit Frontend (Port 8501)               │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                │  │
│  │  │ Input    │  │ Display  │  │  Error   │                │  │
│  │  │ Form     │  │ Results  │  │ Handling │                │  │
│  │  └──────────┘  └──────────┘  └──────────┘                │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTP REST API (JSON)
                           │
┌──────────────────────────┴──────────────────────────────────────┐
│                    COUCHE APPLICATION                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend (Port 8000)                  │  │
│  │                                                           │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │  │
│  │  │ /predict │  │ /health  │  │ /metrics │               │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘               │  │
│  │       │             │              │                      │  │
│  │  ┌────▼────────────────────────────▼─────┐               │  │
│  │  │        Middleware Layer                │               │  │
│  │  │  - CORS                                │               │  │
│  │  │  - Prometheus Metrics                  │               │  │
│  │  │  - Error Handling                      │               │  │
│  │  └────────────────────────────────────────┘               │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────┬──────────┬────────────────────┘
                       │          │          │
         ┌─────────────┴──┐  ┌────┴────┐  ┌─┴────────────┐
         │                │  │         │  │              │
┌────────▼─────────┐  ┌──▼──▼──────┐  │  ┌▼──────────────▼──────┐
│  COUCHE CACHE    │  │COUCHE LOGIC│  │  │  COUCHE MONITORING   │
│                  │  │            │  │  │                      │
│  ┌────────────┐  │  │ ┌────────┐ │  │  │  ┌────────────────┐ │
│  │   Redis    │  │  │ │   ML   │ │  │  │  │  Prometheus    │ │
│  │   Cache    │  │  │ │ Model  │ │  │  │  │   Collector    │ │
│  │ Port 6379  │  │  │ │        │ │  │  │  │   Port 9090    │ │
│  └────────────┘  │  │ └────────┘ │  │  │  └────────┬───────┘ │
│                  │  │            │  │  │           │          │
│  - TTL: 1h       │  │ Random     │  │  │  ┌────────▼───────┐ │
│  - LRU eviction  │  │ Forest     │  │  │  │    Grafana     │ │
└──────────────────┘  └────────────┘  │  │  │   Dashboard    │ │
                                      │  │  │   Port 3000    │ │
                                      │  │  └────────────────┘ │
┌─────────────────────────────────────┘  └─────────────────────┘
│         COUCHE TRAÇABILITÉ
│  ┌────────────────────────────────┐
│  │    Prediction Tracker          │
│  │  - Logs JSONL                  │
│  │  - Audit Trail                 │
│  │  - Model Versioning            │
│  └────────────────────────────────┘
└────────────────────────────────────
```

### 🔄 Diagramme de Séquence - Flux de Prédiction

```
Utilisateur    Frontend     Backend      Redis     ML Model    Prometheus    Logs
    │             │            │           │          │            │          │
    │  1. Saisie  │            │           │          │            │          │
    │─────────────>│            │           │          │            │          │
    │             │            │           │          │            │          │
    │             │ 2. POST    │           │          │            │          │
    │             │  /predict  │           │          │            │          │
    │             │────────────>│           │          │            │          │
    │             │            │           │          │            │          │
    │             │            │ 3. Check  │          │            │          │
    │             │            │  Cache    │          │            │          │
    │             │            │───────────>│          │            │          │
    │             │            │           │          │            │          │
    │             │            │ 4a. MISS  │          │            │          │
    │             │            │<───────────│          │            │          │
    │             │            │           │          │            │          │
    │             │            │ 5. Predict│          │            │          │
    │             │            │──────────────────────>│            │          │
    │             │            │           │          │            │          │
    │             │            │ 6. Price  │          │            │          │
    │             │            │<──────────────────────│            │          │
    │             │            │           │          │            │          │
    │             │            │ 7. Cache  │          │            │          │
    │             │            │  Result   │          │            │          │
    │             │            │───────────>│          │            │          │
    │             │            │           │          │            │          │
    │             │            │ 8. Track Metrics      │            │          │
    │             │            │───────────────────────────────────>│          │
    │             │            │           │          │            │          │
    │             │            │ 9. Log Prediction                  │          │
    │             │            │────────────────────────────────────────────────>│
    │             │            │           │          │            │          │
    │             │ 10. JSON   │           │          │            │          │
    │             │  Response  │           │          │            │          │
    │             │<────────────│           │          │            │          │
    │             │            │           │          │            │          │
    │ 11. Afficher│            │           │          │            │          │
    │<─────────────│            │           │          │            │          │
    │             │            │           │          │            │          │
```

### 🌐 Diagramme de Déploiement Docker

```
┌────────────────────────────────────────────────────────────────┐
│                      Docker Network: monitoring                │
│                                                                │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Frontend        │         │  Backend         │            │
│  │  Container       │         │  Container       │            │
│  │                  │         │                  │            │
│  │  Streamlit       │<──REST──│  FastAPI         │            │
│  │  Port: 8501      │         │  Port: 8000      │            │
│  │                  │         │                  │            │
│  │  Image:          │         │  Image:          │            │
│  │  python:3.11     │         │  python:3.11     │            │
│  └──────────────────┘         └────────┬─────────┘            │
│                                        │                       │
│                          ┌─────────────┼─────────────┐         │
│                          │             │             │         │
│  ┌──────────────────┐    │   ┌─────────▼─────────┐   │         │
│  │  Redis           │<───┴───│  ML Model         │   │         │
│  │  Container       │        │  (In Backend)     │   │         │
│  │                  │        │                   │   │         │
│  │  Image:          │        │  model.joblib     │   │         │
│  │  redis:7-alpine  │        │  49.77 MB         │   │         │
│  │  Port: 6379      │        └───────────────────┘   │         │
│  └────────┬─────────┘                                │         │
│           │                                          │         │
│  ┌────────▼─────────┐    ┌───────────────────┐      │         │
│  │  Prometheus      │    │  Grafana          │      │         │
│  │  Container       │    │  Container        │      │         │
│  │                  │◄───│                   │      │         │
│  │  Image:          │    │  Image:           │      │         │
│  │  prom/prometheus │    │  grafana/grafana  │      │         │
│  │  Port: 9090      │    │  Port: 3000       │      │         │
│  └──────────────────┘    └───────────────────┘      │         │
│                                                      │         │
│  ┌──────────────────┐                                │         │
│  │  Redis Exporter  │                                │         │
│  │  Container       │                                │         │
│  │                  │                                │         │
│  │  Port: 9121      │────────────────────────────────┘         │
│  └──────────────────┘                                          │
│                                                                │
│  Volume Mounts:                                                │
│  - prometheus_data  → /prometheus                              │
│  - grafana_data     → /var/lib/grafana                         │
│  - redis_data       → /data                                    │
└────────────────────────────────────────────────────────────────┘
```

### 📡 Communication entre Services

```
┌──────────────────────────────────────────────────────────┐
│                   FLUX DE DONNÉES                        │
└──────────────────────────────────────────────────────────┘

Requête Utilisateur
       │
       ▼
┌──────────────┐  Port 8501
│  Streamlit   │  Protocol: HTTP
│  Frontend    │  Format: Form Data
└──────┬───────┘
       │
       │ [POST /predict]
       │ Content-Type: application/json
       │ Body: CarFeatures
       │
       ▼
┌──────────────┐  Port 8000
│   FastAPI    │  Protocol: HTTP REST
│   Backend    │  Format: JSON
└──┬────┬───┬──┘
   │    │   │
   │    │   └──────────────────┐
   │    │                      │
   │    │               [GET /metrics]
   │    │                      │
   │    │                      ▼
   │    │              ┌───────────────┐  Port 9090
   │    │              │  Prometheus   │  Protocol: HTTP
   │    │              │   Scraper     │  Format: Text (Metrics)
   │    │              └───────┬───────┘
   │    │                      │
   │    │                      │ [Pull Metrics]
   │    │                      │
   │    │                      ▼
   │    │              ┌───────────────┐  Port 3000
   │    │              │   Grafana     │  Protocol: HTTP
   │    │              │  Dashboards   │  Format: PromQL
   │    │              └───────────────┘
   │    │
   │    │ [Check Cache: GET key]
   │    │ Protocol: Redis Protocol
   │    │
   │    ▼
   │ ┌──────────────┐  Port 6379
   │ │    Redis     │  Protocol: RESP
   │ │    Cache     │  Format: Binary
   │ └──────┬───────┘
   │        │
   │        │ Cache Miss
   │        │
   │        ▼
   │ [Load Model & Predict]
   │
   ▼
┌──────────────┐
│  ML Model    │  In-Memory
│Random Forest │  Format: Joblib
└──────┬───────┘
       │
       │ [Return Prediction]
       │
       ▼
┌──────────────┐
│ Response to  │
│  Frontend    │
└──────────────┘


LÉGENDE:
━━━━  Communication HTTP/REST
═════  Communication Redis
─ ─ ─  Pull/Scrape Metrics
```

### 🔐 Sécurité et Validation

```
┌───────────────────────────────────────────────────┐
│            PIPELINE DE VALIDATION                 │
└───────────────────────────────────────────────────┘

Input (Frontend)
     │
     │ [User Input]
     │
     ▼
┌─────────────────┐
│ Client-Side     │
│ Validation      │
│ - Required      │
│ - Format        │
│ - Range         │
└────────┬────────┘
         │
         │ [Valid]
         │
         ▼
┌─────────────────┐
│ HTTP POST       │
│ with JSON       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FastAPI         │
│ Pydantic Schema │
│ - Type Check    │
│ - Field Validate│
│ - Year: 1990-   │
│   2026          │
└────────┬────────┘
         │
         │ [Valid]
         │
         ▼
┌─────────────────┐
│ Business Logic  │
│ - Cache Check   │
│ - Model Predict │
│ - Log Track     │
└────────┬────────┘
         │
         ▼
    Response
```

### 🎨 Diagrammes de Flux Interactifs (Mermaid)

#### 📊 Flux Principal de Prédiction

```mermaid
graph TD
    A[👤 Utilisateur] --> B[🌐 Interface Streamlit]
    B --> C[📝 Formulaire de Saisie]
    C --> D[✅ Validation Client]
    D --> E{📋 Données Valides?}
    E -->|Non| F[❌ Afficher Erreurs]
    F --> C
    E -->|Oui| G[📤 POST /predict]
    G --> H[🐍 FastAPI Backend]
    H --> I[🔍 Validation Pydantic]
    I --> J{✅ Schéma Valide?}
    J -->|Non| K[❌ HTTP 422]
    K --> B
    J -->|Oui| L[🔎 Vérifier Cache Redis]
    L --> M{💾 Cache Hit?}
    M -->|Oui| N[⚡ Retour Immédiat]
    M -->|Non| O[🤖 Charger ML Model]
    O --> P[🧮 Prédiction Random Forest]
    P --> Q[💾 Mise en Cache]
    Q --> R[📊 Track Prometheus]
    R --> S[📝 Log Prediction]
    S --> T[✅ Retour Prix MAD]
    N --> T
    T --> U[📈 Affichage Résultat]
    U --> A
    
    style A fill:#e1f5ff
    style H fill:#fff4e6
    style O fill:#f3e5f5
    style L fill:#e8f5e9
    style R fill:#fce4ec
    style T fill:#e8f5e9
```

#### 🔄 Flux avec Cache Redis

```mermaid
graph LR
    A[📥 Requête] --> B{🔍 Cache Redis}
    B -->|Hit 🎯| C[⚡ Réponse Instantanée<br/>~5ms]
    B -->|Miss ❌| D[🤖 ML Model]
    D --> E[🧮 Prédiction<br/>~45ms]
    E --> F[💾 Sauvegarder Cache<br/>TTL: 1h]
    F --> G[📤 Réponse]
    C --> H[📊 Metrics: cache_hit++]
    G --> I[📊 Metrics: cache_miss++]
    
    style B fill:#e3f2fd
    style C fill:#c8e6c9
    style D fill:#fff9c4
    style F fill:#ffccbc
```

#### 📈 Flux de Monitoring

```mermaid
graph TD
    A[🌐 Requête HTTP] --> B[⏱️ Middleware Metrics]
    B --> C[📝 Enregistrer Temps Début]
    C --> D[🔄 Traiter Requête]
    D --> E[📝 Enregistrer Temps Fin]
    E --> F[📊 Calculer Latence]
    F --> G[📈 Incrémenter Compteurs]
    G --> H{📊 Type Métrique}
    H -->|Requête| I[http_requests_total++]
    H -->|Latence| J[http_request_duration_seconds]
    H -->|Prédiction| K[predictions_total++]
    H -->|Prix| L[predicted_prices histogram]
    H -->|Cache| M[cache_hits/misses++]
    I --> N[🔍 Prometheus Scrape<br/>Interval: 15s]
    J --> N
    K --> N
    L --> N
    M --> N
    N --> O[📊 Grafana Dashboard]
    O --> P[👀 Visualisation Temps Réel]
    
    style B fill:#e1bee7
    style N fill:#fff59d
    style O fill:#80deea
    style P fill:#a5d6a7
```

#### ⚠️ Flux de Gestion des Erreurs

```mermaid
graph TD
    A[📥 Requête Entrante] --> B{🔍 Type Erreur?}
    B -->|Validation| C[❌ HTTP 422]
    B -->|Model Non Chargé| D[❌ HTTP 503]
    B -->|Erreur Interne| E[❌ HTTP 500]
    B -->|✅ Succès| F[✅ HTTP 200]
    
    C --> G[📝 Log: Validation Error]
    D --> H[📝 Log: Service Unavailable]
    E --> I[📝 Log: Internal Error]
    F --> J[📝 Log: Success]
    
    G --> K[📊 Metrics: errors++]
    H --> K
    I --> K
    
    J --> L[📊 Metrics: success++]
    
    K --> M[🔔 Prometheus Alert?]
    M -->|Seuil Dépassé| N[🚨 Alerte Email/Slack]
    M -->|Normal| O[✅ Surveillance Continue]
    
    L --> O
    
    style C fill:#ffcdd2
    style D fill:#ffcdd2
    style E fill:#ffcdd2
    style F fill:#c8e6c9
    style N fill:#ff6b6b
```

#### 🗄️ Flux de Traçabilité

```mermaid
graph LR
    A[🎯 Prédiction Effectuée] --> B[🔐 Générer ID Unique<br/>SHA256]
    B --> C[📊 Collecter Métadonnées]
    C --> D[📝 Créer Log Entry]
    D --> E{💾 Format}
    E -->|JSON| F[📄 predictions_YYYY-MM-DD.jsonl]
    E -->|Metrics| G[📈 Prometheus Counter]
    E -->|Cache| H[💾 Redis Stats]
    
    F --> I[🗄️ Stockage Local<br/>logs/predictions/]
    G --> J[📊 Grafana Dashboard]
    H --> K[📉 Cache Performance]
    
    I --> L[🔍 Analyse & Audit]
    J --> L
    K --> L
    
    style B fill:#e1f5fe
    style D fill:#fff9c4
    style I fill:#f3e5f5
    style L fill:#c8e6c9
```

#### 🚀 Flux de Déploiement

```mermaid
graph TD
    A[👨‍💻 Développeur] --> B[💻 git push origin main]
    B --> C{🌳 Branche?}
    C -->|main| D[🚀 GitHub Actions CI/CD]
    C -->|autre| E[✅ Push Simple]
    
    D --> F[🧪 Tests Pytest<br/>27 tests]
    F --> G{✅ Tests Passés?}
    G -->|Non| H[❌ Build Failed]
    G -->|Oui| I[🐳 Docker Build]
    
    I --> J[📦 Build Backend Image]
    I --> K[📦 Build Frontend Image]
    
    J --> L[🏗️ Tag: latest]
    K --> L
    
    L --> M{🎯 Destination?}
    M -->|HuggingFace| N[🤗 Deploy to Spaces]
    M -->|Local| O[🐳 Docker Compose up]
    
    N --> P[🌐 Live sur HF Spaces]
    O --> Q[💻 Environnement Local]
    
    H --> R[🔔 Notification Échec]
    
    style D fill:#e3f2fd
    style G fill:#fff9c4
    style N fill:#c8e6c9
    style P fill:#a5d6a7
    style H fill:#ffcdd2
```

#### 🏗️ Architecture des Composants

```mermaid
graph TB
    subgraph Frontend["🌐 FRONTEND LAYER"]
        A[Streamlit UI<br/>Port 8501]
    end
    
    subgraph Backend["⚙️ BACKEND LAYER"]
        B[FastAPI<br/>Port 8000]
        C[Pydantic Schemas]
        D[CORS Middleware]
    end
    
    subgraph Cache["💾 CACHE LAYER"]
        E[Redis<br/>Port 6379]
        F[TTL: 1 hour]
        G[LRU Eviction]
    end
    
    subgraph ML["🤖 ML LAYER"]
        H[Random Forest Model]
        I[model.joblib<br/>49.77 MB]
        J[Scikit-learn 1.6.1]
    end
    
    subgraph Monitoring["📊 MONITORING LAYER"]
        K[Prometheus<br/>Port 9090]
        L[Grafana<br/>Port 3000]
        M[Redis Exporter<br/>Port 9121]
    end
    
    subgraph Logs["📝 LOGGING LAYER"]
        N[Prediction Tracker]
        O[JSONL Files]
        P[Audit Trail]
    end
    
    A -->|HTTP REST| B
    B --> C
    B --> D
    B -->|Check| E
    E --> F
    E --> G
    B -->|Predict| H
    H --> I
    H --> J
    B -->|Metrics| K
    K --> L
    E -->|Stats| M
    M --> K
    B -->|Track| N
    N --> O
    N --> P
    
    style Frontend fill:#e3f2fd
    style Backend fill:#fff9c4
    style Cache fill:#f3e5f5
    style ML fill:#e8f5e9
    style Monitoring fill:#fce4ec
    style Logs fill:#fff3e0
```

---

## 📁 Structure des Dossiers

```
CarPricePredictor-MA/
│
├── 📂 backend/                      # Backend FastAPI
│   ├── app/
│   │   ├── main.py                  # API principale
│   │   ├── schemas.py               # Validation Pydantic
│   │   ├── cache.py                 # Cache Redis
│   │   ├── monitoring.py            # Métriques Prometheus
│   │   └── prediction_tracker.py    # Traçabilité
│   ├── tests/                       # 27 tests unitaires
│   │   ├── test_main.py             # Tests API
│   │   └── test_schemas.py          # Tests schémas
│   └── requirements.txt             # Dépendances
│
├── 📂 frontend/                     # Frontend Streamlit
│   ├── app.py                       # Interface web
│   └── requirements.txt
│
├── 📂 ml/                           # Machine Learning
│   └── artifacts/
│       └── model.joblib             # Modèle (50 MB)
│
├── 📂 notebooks/                    # Jupyter Notebooks
│   ├── CarPrice_ML.ipynb            # Pipeline ML complet
│   └── ReadData.ipynb               # Exploration données
│
├── 📂 data/                         # Données
│   └── DataSet.csv                  # Dataset (898 KB)
│
├── 📂 monitoring/                   # Monitoring
│   ├── docker-compose.monitoring.yml
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alerts.yml
│   └── grafana/
│       └── provisioning/
│
└── 🐳 Dockerfile                    # Hugging Face Spaces
```

---

## 🛠️ Technologies Utilisées

### Backend
- **FastAPI 0.104.1** - Framework web moderne
- **Uvicorn** - Serveur ASGI
- **Pydantic** - Validation de données

### Frontend  
- **Streamlit 1.28.0** - Interface web ML

### Machine Learning
- **scikit-learn 1.6.1** - Framework ML
- **Pandas** - Manipulation de données
- **Joblib** - Sérialisation modèle

### Monitoring
- **Redis 7.0** - Cache en mémoire
- **Prometheus** - Métriques
- **Grafana** - Visualisation

### DevOps
- **Docker** - Containerisation
- **Git LFS** - Gros fichiers
- **Pytest** - Tests unitaires

---

## ✨ Fonctionnalités

### 🎯 Prédiction de Prix
✅ Estimation basée sur 13+ caractéristiques  
✅ Modèle Random Forest optimisé  
✅ Validation temps réel  
✅ Gestion des erreurs

### ⚡ Performance
✅ Cache Redis (90% gain performance)  
✅ Architecture async  
✅ Modèle pré-chargé en mémoire

### 📊 Monitoring
✅ Métriques Prometheus (requêtes, latence, erreurs)  
✅ Dashboards Grafana  
✅ Alertes automatiques  
✅ Cache hit/miss rate

### 📝 Traçabilité
✅ Logs JSON de toutes les prédictions  
✅ ID unique par prédiction  
✅ Historique complet  
✅ Versionnement modèle

### 🧪 Tests
✅ 27 tests unitaires (Pytest)  
✅ Couverture 83%  
✅ Tests endpoints API  
✅ Tests validation schémas

---

## 🚀 Installation

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

## 🎯 Utilisation

### Interface Web

1. Ouvrir http://localhost:8501
2. Remplir le formulaire
3. Cliquer "Estimer le prix (MAD)"
4. Obtenir le prix estimé

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

**Réponse:**
```json
{
  "price_mad": 150000.50
}
```

---

## 📚 API Documentation

### Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/predict` | POST | Prédire le prix |
| `/health` | GET | État du système |
| `/metrics` | GET | Métriques Prometheus |
| `/cache/stats` | GET | Stats cache Redis |
| `/predictions/stats` | GET | Stats prédictions |

### Documentation Interactive

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📊 Monitoring

### Métriques Prometheus

- `http_requests_total` - Total requêtes
- `http_request_duration_seconds` - Latence
- `predictions_total` - Total prédictions
- `cache_hits_total` - Cache hits
- `cache_misses_total` - Cache misses
- `model_loaded` - Statut modèle

### Grafana Dashboards

Ouvrir http://localhost:3000 (admin/admin123)

Dashboards disponibles:
- **API Performance** - Latence, throughput
- **ML Metrics** - Prédictions, prix
- **Cache Performance** - Hit rate
- **System Health** - CPU, RAM

---

## 🧪 Tests

```bash
# Tous les tests
cd backend
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=app --cov-report=html

# Résultat: 27 tests passés, 83% couverture
```

### Tests inclus

- ✅ 17 tests endpoints API
- ✅ 10 tests schémas Pydantic
- ✅ Tests health check
- ✅ Tests prédictions
- ✅ Tests validation

---

## 🚀 Déploiement

### Hugging Face Spaces

Le projet est déployé sur:
🌐 https://huggingface.co/spaces/SaidOuchrif/CarPricePredictor-MA

```bash
# Déployer
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

## 👨‍💻 Contributeur

<div align="center">

### Said Ouchrif

[![GitHub](https://img.shields.io/badge/GitHub-Saidouchrif-181717?logo=github)](https://github.com/Saidouchrif)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Said_Ouchrif-0A66C2?logo=linkedin)](https://linkedin.com/in/saidouchrif)
[![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-SaidOuchrif-FFD21E)](https://huggingface.co/SaidOuchrif)

**Data Scientist & ML Engineer**

Passionné par le Machine Learning et le développement d'applications intelligentes.

</div>

---

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📞 Contact

- 📧 Email: saidouchrif16@gmail.com
- 🐙 GitHub: [@Saidouchrif](https://github.com/Saidouchrif)
- 🤗 Hugging Face: [@SaidOuchrif](https://huggingface.co/SaidOuchrif)

---

## 🙏 Remerciements

- Dataset de voitures d'occasion au Maroc
- Communauté scikit-learn
- FastAPI et Streamlit
- Hugging Face pour l'hébergement

---

<div align="center">

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile! ⭐**

Made with ❤️ by [Said Ouchrif](https://github.com/Saidouchrif)

</div>
