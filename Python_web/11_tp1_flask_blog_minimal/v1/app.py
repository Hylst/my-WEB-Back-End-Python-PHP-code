from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

# 01/12/2023 - Geoffroy
# TP1 - Version 1 : Le Blog Minimaliste.
# C'est un grand classique. On commence petit.
# Pour l'instant, les articles sont stockés en RAM (liste Python).
# Si le serveur restart, pouf, plus d'articles. C'est un blog éphémère, poétique non ?

app = Flask(__name__)

# Notre base de données très volatile.
articles = [
    {
        "id": 1,
        "titre": "Bienvenue sur mon Codex",
        "contenu": "Ceci est le tout premier article. Flask est fun !",
        "date": "2023-12-01"
    }
]

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titre = request.form['titre']
        contenu = request.form['contenu']
        if titre and contenu:
            # On génère un ID unique (en supposant qu'on ne supprime rien pour l'instant)
            new_id = len(articles) + 1
            new_article = {
                "id": new_id,
                "titre": titre,
                "contenu": contenu,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            articles.append(new_article)
            # Retour à l'accueil
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/article/<int:id>')
def view_article(id):
    # Recherche simple. Pas très opti mais ça passe.
    article = next((a for a in articles if a['id'] == id), None)
    if article:
        return render_template('article.html', article=article)
    return "Article introuvable (404 - Échec critique de perception)", 404

if __name__ == "__main__":
    app.run(debug=True)
