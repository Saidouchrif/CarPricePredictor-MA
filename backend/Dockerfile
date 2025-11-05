FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances
COPY backend/requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY backend/app/ ./app/

# Créer le répertoire pour le modèle (sera monté via volume)
RUN mkdir -p ./ml/artifacts

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]