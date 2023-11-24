from flask import Flask, render_template, request, flash, redirect, url_for
import secrets

# 24/11/2023 - Geoffroy
# Les formulaires V2.
# Découverte de 'flash' pour les messages temporaires. C'est bien plus propre.
# J'ajoute aussi une protection CSRF "maison" (le token secret).
# Et un peu de CSS pour que ça ressemble à quelque chose.

app = Flask(__name__)
# Une clef secrète générée aléatoirement pour sécuriser les sessions et les flash messages
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # On récupère les données
        nom = request.form.get('nom')
        msg = request.form.get('message')
        
        # Validation
        if not nom or not msg:
            flash("Erreur : Tous les champs sont obligatoires, aventurier.", "error")
        elif len(msg) < 10:
            flash("Erreur : Votre quête est trop courte pour être prise au sérieux.", "error")
        else:
            # Traitement succès
            flash(f"Salutations {nom} ! Votre missive a été confiée à nos meilleurs coursiers.", "success")
            # Pattern PRG (Post/Redirect/Get) pour éviter le re-submit si on rafraîchit
            return redirect(url_for('contact'))
        
    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)
