from flask import Flask, jsonify, request, abort
from functools import wraps
import time

# 26/11/2023 - Geoffroy
# Mini API V2 - Plus REST-compliant
# J'ai structuré les réponses avec un format standard (data/meta/error).
# Ajout d'un middleware de timing pour mesurer les performances.
# C'est le genre de chose qu'on voit en production, je m'entraîne.

app = Flask(__name__)

# ============================================
# Données simulées (en attendant SQLite)
# ============================================
INVENTORY = [
    {"id": 1, "name": "Épée longue", "type": "Arme", "damage": "1d8", "price": 15},
    {"id": 2, "name": "Potion de soin", "type": "Consommable", "heal": "2d4+2", "price": 50},
    {"id": 3, "name": "Corde (15m)", "type": "Outil", "utility": "Indispensable", "price": 1},
    {"id": 4, "name": "Torche", "type": "Outil", "duration": "1h", "price": 0.5}
]

# ============================================
# Helpers pour réponses standardisées
# ============================================
def api_response(data, status=200, meta=None):
    """Format de réponse standard pour l'API."""
    response = {
        "success": True,
        "data": data,
        "meta": meta or {}
    }
    return jsonify(response), status

def api_error(message, status=400, code="BAD_REQUEST"):
    """Format d'erreur standard."""
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }
    return jsonify(response), status

def timing_decorator(f):
    """Mesure le temps d'exécution de l'endpoint."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        elapsed = round((time.time() - start) * 1000, 2)
        # On pourrait logger ça aussi
        return result
    return wrapper

# ============================================
# Routes API
# ============================================
@app.route('/api/v1/status')
@timing_decorator
def status():
    return api_response({
        "service": "Flask Mini API",
        "version": "2.0.0",
        "status": "OPERATIONAL"
    })

@app.route('/api/v1/inventory')
@timing_decorator
def get_inventory():
    # Filtrage optionnel par type
    item_type = request.args.get('type')
    items = INVENTORY
    
    if item_type:
        items = [i for i in INVENTORY if i['type'].lower() == item_type.lower()]
    
    return api_response(items, meta={"count": len(items)})

@app.route('/api/v1/inventory/<int:item_id>')
@timing_decorator
def get_item(item_id):
    item = next((i for i in INVENTORY if i['id'] == item_id), None)
    if not item:
        return api_error(f"Item #{item_id} introuvable", 404, "NOT_FOUND")
    return api_response(item)

@app.route('/api/v1/inventory', methods=['POST'])
@timing_decorator
def add_item():
    if not request.is_json:
        return api_error("Content-Type doit être application/json", 415, "UNSUPPORTED_MEDIA")
    
    data = request.get_json()
    required = ['name', 'type', 'price']
    missing = [f for f in required if f not in data]
    
    if missing:
        return api_error(f"Champs manquants : {', '.join(missing)}", 400, "VALIDATION_ERROR")
    
    new_id = max(i['id'] for i in INVENTORY) + 1
    new_item = {"id": new_id, **data}
    INVENTORY.append(new_item)
    
    return api_response(new_item, 201, meta={"message": "Item créé avec succès"})

# ============================================
# Gestionnaires d'erreurs globaux
# ============================================
@app.errorhandler(404)
def not_found(e):
    return api_error("Endpoint non trouvé", 404, "NOT_FOUND")

@app.errorhandler(500)
def server_error(e):
    return api_error("Erreur interne du serveur", 500, "INTERNAL_ERROR")

if __name__ == "__main__":
    app.run(debug=True)
