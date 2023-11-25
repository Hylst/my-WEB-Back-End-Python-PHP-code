from flask import Flask, abort
from werkzeug.routing import BaseConverter

# 25/11/2023 - Geoffroy
# Routing V2 : Custom Converters.
# J'ai appris qu'on pouvait créer ses propres types de variables d'URL.
# Utile pour valider des formats spécifiques (comme une liste de codes séparés par des virgules).
# C'est du "Regex on steroids" pour les routes.

class ListConverter(BaseConverter):
    """Convertit une partie d'URL séparée par '+' en liste Python."""
    def to_python(self, value):
        return value.split('+')
    
    def to_url(self, value):
        return '+'.join(BaseConverter.to_url(value))

app = Flask(__name__)
# On enregistre notre convertisseur magique
app.url_map.converters['list'] = ListConverter

@app.route('/')
def index():
    return """
    <h1>Système de Navigation Avancé</h1>
    <ul>
        <li><a href="/user/42">Profil User 42</a></li>
        <li><a href="/items/epee+bouclier+potion">Inventaire (Liste)</a></li>
        <li><a href="/article/le-retour-du-roi">Article (Slug)</a></li>
    </ul>
    """

@app.route('/user/<int:user_id>')
def show_user(user_id):
    if user_id > 100:
        abort(404, description="ID hors limites (Max 100)")
    return f"<h2>Connexion au profil #{user_id}</h2>"

@app.route('/items/<list:items>')
def show_inventory(items):
    # 'items' est directement une liste Python ici !
    html_list = "".join([f"<li>{item}</li>" for item in items])
    return f"<h2>Inventaire du sac :</h2><ul>{html_list}</ul>"

@app.route('/article/<path:slug>')
def show_article(slug):
    # 'path' permet d'accepter les slashs aussi, contrairement à string par défaut
    return f"<h2>Lecture de : {slug}</h2>"

@app.errorhandler(404)
def page_not_found(e):
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: monospace;">
        <h1>🛑 404 - ZONE INTERDITE</h1>
        <p>{e.description}</p>
        <p><i>Ce n'est pas la route que vous recherchez...</i></p>
        <a href="/">Retour au campement</a>
    </div>
    """, 404

if __name__ == "__main__":
    app.run(debug=True)
