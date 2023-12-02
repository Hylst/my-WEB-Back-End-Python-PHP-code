from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

# 02/12/2023 - Geoffroy
# TP1 - Version 2 : Persistance JSON.
# Adieu l'amnésie du serveur. Maintenant on écrit tout dans 'data.json'.
# C'est un peu "crado" comparé à une DB, mais pour un petit projet perso, ça fait le café.
# J'ai ajouté des fonctions load/save pour structurer un peu.

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    articles = load_data()
    return render_template('index.html', articles=articles)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titre = request.form['titre']
        contenu = request.form['contenu']
        if titre and contenu:
            articles = load_data()
            new_id = len(articles) + 1
            new_article = {
                "id": new_id,
                "titre": titre,
                "contenu": contenu,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            articles.append(new_article)
            save_data(articles)
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/article/<int:id>')
def view_article(id):
    articles = load_data()
    article = next((a for a in articles if a['id'] == id), None)
    if article:
        return render_template('article.html', article=article)
    return "Article introuvable", 404

if __name__ == "__main__":
    app.run(debug=True)
