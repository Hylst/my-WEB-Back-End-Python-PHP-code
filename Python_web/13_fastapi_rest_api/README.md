# Exercice 13 : FastAPI REST API

## Description
API RESTful complète pour gérer des quêtes héroïques.

## Fonctionnalités
- CRUD complet sur les quêtes
- Validation automatique avec Pydantic
- Documentation Swagger auto-générée
- Filtres et pagination
- Actions spéciales (accept, complete)
- Statistiques

## Installation
```bash
pip install -r requirements.txt
```

## Lancement
```bash
uvicorn main:app --reload
```

## Documentation
- Swagger UI : http://127.0.0.1:8000/docs
- ReDoc : http://127.0.0.1:8000/redoc

## Endpoints
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | /api/quests | Liste des quêtes |
| GET | /api/quests/{id} | Détail d'une quête |
| POST | /api/quests | Créer une quête |
| PATCH | /api/quests/{id} | Modifier une quête |
| DELETE | /api/quests/{id} | Supprimer une quête |
| POST | /api/quests/{id}/accept | Accepter une quête |
| POST | /api/quests/{id}/complete | Terminer une quête |
| GET | /api/stats | Statistiques |
