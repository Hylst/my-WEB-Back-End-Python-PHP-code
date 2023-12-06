# Exercice 14 : Flask API Client

## Description
Frontend Flask qui consomme l'API FastAPI de l'exercice 13.

## Architecture
```
[Navigateur] <-> [Flask :5000] <-> [FastAPI :8000]
```

## Prérequis
L'API FastAPI (exercice 13) doit tourner sur http://127.0.0.1:8000

## Installation
```bash
pip install -r requirements.txt
```

## Lancement
```bash
# Terminal 1 - API Backend (Ex 13)
cd ../13_fastapi_rest_api
uvicorn main:app --reload

# Terminal 2 - Frontend Flask (Ex 14)
python app.py
```

## Fonctionnalités
- Liste des quêtes avec filtres
- Création / Modification / Suppression
- Actions : Accepter, Terminer
- Statistiques en temps réel
- Gestion d'erreurs API

## Points techniques
- Service Layer pour encapsuler les appels API
- Gestion des erreurs réseau
- Flash messages pour feedback utilisateur
- CSS GitHub-like dark theme
