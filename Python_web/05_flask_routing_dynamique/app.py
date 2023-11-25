from flask import Flask

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
    # Ici, on simulerait une recherche en BDD.
    # Pour l'instant, on imagine.
    return f"<h2>Profil du joueur niveau {user_id}</h2>"

@app.route('/article/<slug>')
def show_article(slug):
    # Le slug est comme le nom de code de la mission.
    formatted_slug = slug.replace('-', ' ')
    return f"<h2>Lecture du parchemin : {formatted_slug.capitalize()}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
