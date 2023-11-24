from flask import Flask, render_template, request

# 24/11/2023 - Geoffroy
# Les formulaires. C'est là que l'utilisateur entre en scène.
# Attention aux entrées utilisateurs, c'est comme laisser un joueur lancer ses dés derrière l'écran du MJ.
# Toujours vérifier. Ici on reste simple (GET/POST).

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def contact():
    message_sent = False
    error = None
    
    if request.method == 'POST':
        # On récupère les données du formulaire
        nom = request.form.get('nom')
        msg = request.form.get('message')
        
        # Validation basique
        if not nom or not msg:
            error = "Hé oh, il faut remplir tous les champs !"
        else:
            print(f"Nouveau message de {nom} : {msg}")
            message_sent = True
        
    return render_template('form.html', success=message_sent, error=error)

if __name__ == "__main__":
    app.run(debug=True)
