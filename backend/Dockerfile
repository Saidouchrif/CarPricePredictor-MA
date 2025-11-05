FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances
COPY backend/requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY backend/app/ ./app/

# Créer le répertoire pour le modèle
RUN mkdir -p ./ml/artifacts

# Copier le modèle directement dans l'image (alternative au volume)
COPY ml/artifacts/model.joblib ./ml/artifacts/model.joblib

# Vérifier que le modèle est bien copié
RUN ls -lah ./ml/artifacts/model.joblib

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]