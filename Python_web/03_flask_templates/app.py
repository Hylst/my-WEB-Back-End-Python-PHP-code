from flask import Flask, render_template

# 23/11/2023 - Geoffroy
# Les templates. Très important.
# Ça permet de ne pas mélanger les règles (Python) et le plateau de jeu (HTML).
# Une bonne séparation des préoccupations, comme dans une équipe équilibrée (Tank/Healer/DPS).

app = Flask(__name__)

@app.route('/')
def home():
    user_name = "Voyageur"
    # On passe des variables au template, comme on distribue des cartes aux joueurs.
    return render_template('home.html', name=user_name)

if __name__ == "__main__":
    app.run(debug=True)
