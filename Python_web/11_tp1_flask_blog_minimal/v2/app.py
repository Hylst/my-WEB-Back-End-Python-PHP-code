from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import secrets
import json
import os

# 02/12/2023 - Geoffroy
# TP1 V2 - Blog avec persistance JSON et architecture propre
# Séparation des concerns : les données dans un fichier, la logique dans l'app.
# Ajout d'édition et suppression d'articles.

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
CATEGORIES = ["General", "Tutoriel", "Aventure", "Réflexion", "Tech"]

# ============================================
# Helpers pour la persistance
# ============================================
def load_articles():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_articles(articles):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

def get_next_id(articles):
    return max((a['id'] for a in articles), default=0) + 1

# ============================================
# Routes
# ============================================
@app.route('/')
def index():
    articles = load_articles()
    cat_filter = request.args.get('cat')
    search = request.args.get('q', '').lower()
    
    if cat_filter:
        articles = [a for a in articles if a.get('categorie') == cat_filter]
    if search:
        articles = [a for a in articles if search in a['titre'].lower() or search in a['contenu'].lower()]
    
    articles.sort(key=lambda x: x['date'], reverse=True)
    return render_template('index.html', 
        articles=articles, 
        categories=CATEGORIES,
        current_cat=cat_filter,
        search_query=search
    )

@app.route('/article/<int:id>')
def view_article(id):
    articles = load_articles()
    article = next((a for a in articles if a['id'] == id), None)
    if not article:
        flash("Article introuvable", "error")
        return redirect(url_for('index'))
    
    # Incrémenter les vues
    article['vues'] = article.get('vues', 0) + 1
    save_articles(articles)
    
    return render_template('article.html', article=article)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titre = request.form.get('titre', '').strip()
        contenu = request.form.get('contenu', '').strip()
        categorie = request.form.get('categorie', 'General')
        
        if len(titre) < 3:
            flash("Le titre doit faire au moins 3 caractères", "error")
        elif len(contenu) < 10:
            flash("Le contenu est trop court", "error")
        else:
            articles = load_articles()
            new_article = {
                "id": get_next_id(articles),
                "titre": titre,
                "contenu": contenu,
                "auteur": "Geoffroy",
                "categorie": categorie,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "vues": 0
            }
            articles.append(new_article)
            save_articles(articles)
            flash(f"Article '{titre}' publié !", "success")
            return redirect(url_for('index'))
    
    return render_template('add.html', categories=CATEGORIES)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    articles = load_articles()
    article = next((a for a in articles if a['id'] == id), None)
    if not article:
        flash("Article introuvable", "error")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        article['titre'] = request.form.get('titre', article['titre'])
        article['contenu'] = request.form.get('contenu', article['contenu'])
        article['categorie'] = request.form.get('categorie', article['categorie'])
        save_articles(articles)
        flash("Article mis à jour", "success")
        return redirect(url_for('view_article', id=id))
    
    return render_template('edit.html', article=article, categories=CATEGORIES)

@app.route('/delete/<int:id>')
def delete(id):
    articles = load_articles()
    articles = [a for a in articles if a['id'] != id]
    save_articles(articles)
    flash("Article supprimé", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
