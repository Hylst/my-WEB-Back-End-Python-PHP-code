from flask import Flask, Response, jsonify

# 22/11/2023 - Geoffroy
# Le fameux Hello World.
# C'est un peu le "Roll for Initiative" du dev web.
# On vérifie juste que le serveur répond correctement.
# Update : Ajout d'une route /status pour vérifier que tout est vert.

app = Flask(__name__)

@app.route('/')
def hello():
    # J'utilise Response pour être explicite, comme quand on déclare ses actions au MJ.
    return Response("Hello World! Le serveur Flask est en ligne.", mimetype='text/plain')

@app.route('/status')
def status():
    # Petit check rapide en JSON.
    return jsonify({"server": "up", "level": 1, "class": "Flask"})

if __name__ == "__main__":
    # Debug=True, c'est comme jouer avec l'écran du MJ baissé pour apprendre.
    app.run(debug=True)
