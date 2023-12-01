from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import secrets

# 01/12/2023 - Geoffroy
# TP1 V1 - Blog Amélioré
# Structure plus propre avec des vrais templates séparés.
# Ajout de catégories et de la gestion des erreurs.

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Base de données en mémoire
articles = [
    {
        "id": 1,
        "titre": "Bienvenue sur mon Codex",
        "contenu": "Ceci est le tout premier article. Flask est fun ! Je découvre petit à petit les joies du développement web avec Python.",
        "auteur": "Geoffroy",
        "categorie": "General",
        "date": "2023-12-01",
        "vues": 42
    },
    {
        "id": 2,
        "titre": "Les Secrets de Jinja2",
        "contenu": "Le moteur de templates Jinja2 est vraiment puissant. Héritage, macros, filtres... C'est comme apprendre un nouveau sort.",
        "auteur": "Geoffroy",
        "categorie": "Tutoriel",
        "date": "2023-12-01",
        "vues": 15
    }
]

CATEGORIES = ["General", "Tutoriel", "Aventure", "Réflexion"]

def get_next_id():
    return max(a['id'] for a in articles) + 1 if articles else 1

@app.route('/')
def index():
    cat_filter = request.args.get('cat')
    filtered = articles
    if cat_filter:
        filtered = [a for a in articles if a['categorie'] == cat_filter]
    return render_template('index.html', 
        articles=sorted(filtered, key=lambda x: x['date'], reverse=True),
        categories=CATEGORIES,
        current_cat=cat_filter
    )

@app.route('/article/<int:id>')
def view_article(id):
    article = next((a for a in articles if a['id'] == id), None)
    if not article:
        flash("Article introuvable", "error")
        return redirect(url_for('index'))
    article['vues'] += 1
    return render_template('article.html', article=article)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titre = request.form.get('titre', '').strip()
        contenu = request.form.get('contenu', '').strip()
        categorie = request.form.get('categorie', 'General')
        
        if not titre or not contenu:
            flash("Titre et contenu obligatoires", "error")
        else:
            new_article = {
                "id": get_next_id(),
                "titre": titre,
                "contenu": contenu,
                "auteur": "Geoffroy",
                "categorie": categorie,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "vues": 0
            }
            articles.append(new_article)
            flash(f"Article '{titre}' créé !", "success")
            return redirect(url_for('index'))
    
    return render_template('add.html', categories=CATEGORIES)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
