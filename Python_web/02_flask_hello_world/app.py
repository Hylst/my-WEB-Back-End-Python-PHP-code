from flask import Flask, Response

# 22/11/2023 - Geoffroy
# Le fameux Hello World.
# C'est un peu le "Roll for Initiative" du dev web.
# On vérifie juste que le serveur répond correctement.

app = Flask(__name__)

@app.route('/')
def hello():
    # J'utilise Response pour être explicite, comme quand on déclare ses actions au MJ.
    return Response("Hello World! Le serveur Flask est en ligne.", mimetype='text/plain')

if __name__ == "__main__":
    # Debug=True, c'est comme jouer avec l'écran du MJ baissé pour apprendre.
    app.run(debug=True)
