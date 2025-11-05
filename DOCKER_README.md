# 🐳 Guide Docker - CarPricePredictor-MA

## 📋 Prérequis

- Docker Desktop installé sur Windows
- Le fichier `ml/artifacts/model.joblib` doit exister (entraîner le modèle avec le notebook)

## 🚀 Démarrer l'application complète

### Option 1: Avec Docker Compose (recommandé)

```bash
# À la racine du projet
docker-compose up --build
```

Cette commande va :
- ✅ Construire les images Docker pour backend et frontend
- ✅ Démarrer le backend sur `http://localhost:8000`
- ✅ Démarrer le frontend sur `http://localhost:8501`
- ✅ Créer un réseau pour que les conteneurs communiquent

**Attendez de voir** :
```
carprice-backend   | ✅ Modèle chargé: ...
carprice-frontend  | You can now view your Streamlit app in your browser.
```

### Option 2: En mode détaché (arrière-plan)

```bash
docker-compose up -d
```

Pour voir les logs :
```bash
docker-compose logs -f
```

## 🧪 Tester l'application

1. **Backend (API)** : `http://localhost:8000/docs`
2. **Frontend (Interface)** : `http://localhost:8501`

## 🛑 Arrêter l'application

```bash
# Arrêter les conteneurs
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

## 🔧 Commandes utiles

### Voir les conteneurs en cours d'exécution
```bash
docker-compose ps
```

### Reconstruire uniquement un service
```bash
docker-compose build backend
docker-compose build frontend
```

### Redémarrer un service
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Voir les logs d'un service spécifique
```bash
docker-compose logs backend
docker-compose logs frontend
```

### Accéder au shell d'un conteneur
```bash
docker-compose exec backend bash
docker-compose exec frontend bash
```

## 📂 Structure des services

### Backend (FastAPI)
- **Port** : 8000
- **Image** : python:3.11-slim
- **Volume** : `./ml/artifacts` monté en lecture seule
- **Health check** : `/health` endpoint

### Frontend (Streamlit)
- **Port** : 8501
- **Image** : python:3.11-slim
- **Variable d'env** : `API_URL=http://backend:8000`
- **Dépend de** : Backend

## 🐛 Dépannage

### Le modèle n'est pas chargé
```bash
# Vérifier que le fichier existe
dir ml\artifacts\model.joblib

# Si absent, réentraîner le modèle dans le notebook
```

### Port déjà utilisé
```bash
# Changer les ports dans docker-compose.yml
ports:
  - "8001:8000"  # Backend sur 8001
  - "8502:8501"  # Frontend sur 8502
```

### Frontend ne peut pas contacter le backend
```bash
# Vérifier que les conteneurs sont sur le même réseau
docker network ls
docker network inspect carpricepredictorma_app-network
```

## 🌐 Déploiement en production

Pour déployer sur un serveur :

1. Copier le projet sur le serveur
2. S'assurer que Docker et Docker Compose sont installés
3. Exécuter :
```bash
docker-compose -f docker-compose.yml up -d
```

## 📊 Monitoring

Voir l'utilisation des ressources :
```bash
docker stats
```

## 🔄 Mise à jour

Après modification du code :
```bash
docker-compose down
docker-compose build
docker-compose up -d
```
