from flask import Flask, jsonify

# 26/11/2023 - Geoffroy
# Mini API.
# Le JSON c'est un peu l'Esperanto des machines.
# Pas besoin de fioritures (HTML/CSS), juste de la donnée pure.
# Idéal pour refiler des infos à un front-end qui fait sa vie de son côté.

app = Flask(__name__)

@app.route('/api/inventory')
def get_inventory():
    # Notre inventaire simulé.
    loot = [
        {"id": 1, "name": "Épée longue", "type": "Arme", "damage": "1d8"},
        {"id": 2, "name": "Potion de soin", "type": "Consommable", "heal": "2d4+2"},
        {"id": 3, "name": "Corde (15m)", "type": "Outil", "utility": "Indispensable"}
    ]
    # jsonify s'occupe de transformer notre liste Python en JSON propre.
    return jsonify(loot)

@app.route('/api/status')
def get_status():
    return jsonify({"status": "OK", "hp": "100%", "mana": "80%"})

if __name__ == "__main__":
    app.run(debug=True)
