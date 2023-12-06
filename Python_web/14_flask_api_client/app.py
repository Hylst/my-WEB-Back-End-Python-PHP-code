from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import secrets

# 06/12/2023 - Geoffroy
# Exercice 14 : Flask comme Client API
# Ici Flask joue le rôle de "frontend" qui consomme l'API FastAPI.
# C'est une architecture classique : API backend + Frontend séparé.
# Ça permet de scaler indépendamment les deux parties.

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# URL de l'API FastAPI (à lancer en parallèle)
API_BASE_URL = "http://127.0.0.1:8000/api"

# ============================================
# Service Layer - Encapsule les appels API
# ============================================
class QuestService:
    """Service pour interagir avec l'API Quest Manager."""
    
    @staticmethod
    def get_all(status=None, difficulty=None):
        """Récupère toutes les quêtes."""
        params = {}
        if status:
            params['status'] = status
        if difficulty:
            params['difficulty'] = difficulty
        
        try:
            response = requests.get(f"{API_BASE_URL}/quests", params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_one(quest_id):
        """Récupère une quête par ID."""
        try:
            response = requests.get(f"{API_BASE_URL}/quests/{quest_id}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            return None
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    @staticmethod
    def create(data):
        """Crée une nouvelle quête."""
        try:
            response = requests.post(f"{API_BASE_URL}/quests", json=data, timeout=5)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": e.response.json().get("detail", str(e))}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def update(quest_id, data):
        """Met à jour une quête."""
        try:
            response = requests.patch(f"{API_BASE_URL}/quests/{quest_id}", json=data, timeout=5)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": e.response.json().get("detail", str(e))}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete(quest_id):
        """Supprime une quête."""
        try:
            response = requests.delete(f"{API_BASE_URL}/quests/{quest_id}", timeout=5)
            response.raise_for_status()
            return {"success": True}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def accept(quest_id):
        """Accepte une quête."""
        try:
            response = requests.post(f"{API_BASE_URL}/quests/{quest_id}/accept", timeout=5)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": e.response.json().get("detail", str(e))}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def complete(quest_id):
        """Termine une quête."""
        try:
            response = requests.post(f"{API_BASE_URL}/quests/{quest_id}/complete", timeout=5)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": e.response.json().get("detail", str(e))}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_stats():
        """Récupère les statistiques."""
        try:
            response = requests.get(f"{API_BASE_URL}/stats", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return {}

# ============================================
# Routes Flask
# ============================================
@app.route('/')
def index():
    """Page d'accueil - Liste des quêtes."""
    status_filter = request.args.get('status')
    difficulty_filter = request.args.get('difficulty')
    
    quests = QuestService.get_all(status=status_filter, difficulty=difficulty_filter)
    stats = QuestService.get_stats()
    
    if isinstance(quests, dict) and "error" in quests:
        flash(f"⚠️ Erreur API : {quests['error']}", "error")
        quests = []
    
    return render_template('index.html', 
        quests=quests, 
        stats=stats,
        current_status=status_filter,
        current_difficulty=difficulty_filter
    )

@app.route('/quest/<int:quest_id>')
def quest_detail(quest_id):
    """Détail d'une quête."""
    quest = QuestService.get_one(quest_id)
    if not quest:
        flash("Quête introuvable", "error")
        return redirect(url_for('index'))
    return render_template('detail.html', quest=quest)

@app.route('/quest/new', methods=['GET', 'POST'])
def quest_new():
    """Créer une nouvelle quête."""
    if request.method == 'POST':
        data = {
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "difficulty": request.form.get('difficulty', 'medium'),
            "reward_gold": int(request.form.get('reward_gold', 100))
        }
        deadline = request.form.get('deadline')
        if deadline:
            data['deadline'] = deadline
        
        result = QuestService.create(data)
        if result['success']:
            flash(f"✅ Quête '{data['title']}' créée !", "success")
            return redirect(url_for('index'))
        else:
            flash(f"❌ Erreur : {result['error']}", "error")
    
    return render_template('form.html', quest=None)

@app.route('/quest/<int:quest_id>/edit', methods=['GET', 'POST'])
def quest_edit(quest_id):
    """Modifier une quête."""
    quest = QuestService.get_one(quest_id)
    if not quest:
        flash("Quête introuvable", "error")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = {
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "difficulty": request.form.get('difficulty'),
            "reward_gold": int(request.form.get('reward_gold', 100))
        }
        
        result = QuestService.update(quest_id, data)
        if result['success']:
            flash("✅ Quête mise à jour", "success")
            return redirect(url_for('quest_detail', quest_id=quest_id))
        else:
            flash(f"❌ Erreur : {result['error']}", "error")
    
    return render_template('form.html', quest=quest)

@app.route('/quest/<int:quest_id>/delete')
def quest_delete(quest_id):
    """Supprimer une quête."""
    result = QuestService.delete(quest_id)
    if result['success']:
        flash("🗑️ Quête supprimée", "success")
    else:
        flash(f"❌ Erreur : {result.get('error')}", "error")
    return redirect(url_for('index'))

@app.route('/quest/<int:quest_id>/accept')
def quest_accept(quest_id):
    """Accepter une quête."""
    result = QuestService.accept(quest_id)
    if result['success']:
        flash("⚔️ Quête acceptée ! Bonne chance, aventurier.", "success")
    else:
        flash(f"❌ {result['error']}", "error")
    return redirect(url_for('index'))

@app.route('/quest/<int:quest_id>/complete')
def quest_complete(quest_id):
    """Terminer une quête."""
    result = QuestService.complete(quest_id)
    if result['success']:
        flash("🏆 Quête terminée ! Récompense obtenue.", "success")
    else:
        flash(f"❌ {result['error']}", "error")
    return redirect(url_for('index'))

@app.errorhandler(Exception)
def handle_error(e):
    flash(f"Une erreur est survenue : {str(e)}", "error")
    return redirect(url_for('index'))

if __name__ == "__main__":
    print("⚠️ Assurez-vous que l'API FastAPI tourne sur http://127.0.0.1:8000")
    app.run(port=5000, debug=True)
