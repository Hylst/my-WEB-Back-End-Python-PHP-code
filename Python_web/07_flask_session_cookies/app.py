from flask import Flask, session, redirect, url_for

# 27/11/2023 - Geoffroy
# Sessions et Cookies.
# C'est comme la fiche de perso qu'on garde entre deux séances de jeu.
# Important : ne jamais stocker de secrets critiques ici sans chiffrer (Flask le fait via secret_key mais prudence).

app = Flask(__name__)
# Secret key indispensable pour chiffrer la session côté client.
app.secret_key = 'une_clef_secrete_digne_du_mordor'

@app.route('/')
def home():
    # On récupère le compteur, 0 par défaut.
    count = session.get('visites', 0)
    return f"""
    <h1>Compteur de visites</h1>
    <p>Vous avez visité cette taverne {count} fois.</p>
    <a href="/visit">Entrer à nouveau</a> | <a href="/reset">Oublier tout (Amnésie)</a>
    """

@app.route('/visit')
def visit():
    # On incrémente le compteur dans la session.
    session['visites'] = session.get('visites', 0) + 1
    return redirect(url_for('home'))

@app.route('/reset')
def reset():
    # On vide la session (pop).
    session.pop('visites', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
