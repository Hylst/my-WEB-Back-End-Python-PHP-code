from flask import Flask, abort

# 25/11/2023 - Geoffroy
# Routing dynamique.
# Pour gérer des fiches de persos ou des articles à la volée.
# C'est plus élégant que de faire une page par monstre du bestiaire.

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Bienvenue à l'auberge</h1><p>Essayez /user/1 ou /article/mon-super-article</p>"

@app.route('/user/<int:user_id>')
def show_user(user_id):
    # Simulation de BDD
    if user_id > 100:
        # On ne connaît pas ce joueur > 404
        abort(404, description="Joueur introuvable dans les archives")
    return f"<h2>Profil du joueur niveau {user_id}</h2>"

@app.route('/article/<slug>')
def show_article(slug):
    # Le slug est comme le nom de code de la mission.
    formatted_slug = slug.replace('-', ' ')
    return f"<h2>Lecture du parchemin : {formatted_slug.capitalize()}</h2>"

@app.errorhandler(404)
def page_not_found(e):
    return f"<h1>404 - Perdu dans les limbes</h1><p>{e.description}</p>", 404

if __name__ == "__main__":
    app.run(debug=True)
