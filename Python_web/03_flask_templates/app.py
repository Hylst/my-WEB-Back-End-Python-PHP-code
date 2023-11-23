from flask import Flask, render_template

# 23/11/2023 - Geoffroy
# Les templates V2 - Avec du style (CSS) !
# J'ai ajouté un dossier static/ pour les assets.
# Et on passe des structures de données complexes (listes de dictionnaires) pour tester les boucles Jinja.

app = Flask(__name__)

@app.route('/')
def home():
    user_name = "Voyageur"
    return render_template('home.html', name=user_name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    # Simulation d'une équipe récupérée en base
    members = [
        {"name": "Geoffroy", "role": "Mage Codeur", "level": 5},
        {"name": "Flask", "role": "Framework Agile", "level": 10},
        {"name": "Jinja", "role": "Moteur de Rendu", "level": 8}
    ]
    return render_template('team.html', members=members)

if __name__ == "__main__":
    app.run(debug=True)
