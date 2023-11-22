from flask import Flask, Response, jsonify, request
import logging
from config import DevelopmentConfig

# 22/11/2023 - Geoffroy
# Hello World V3 - "Over-engineered" edition.
# J'ai ajouté un système de logs et une config modulaire.
# C'est peut-être trop pour un hello world, mais je mets en place les bonnes habitudes.
# "Qui peut le plus peut le moins."

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.route('/')
def hello():
    logger.info(f"Visite sur la racine depuis {request.remote_addr}")
    return Response("Hello World! Le système est nominal.", mimetype='text/plain')

@app.route('/status')
def status():
    # Health check enrichi
    status_data = {
        "status": "UP",
        "service": "Flask-Hello-World",
        "version": "1.0.2",
        "environment": app.config['ENV'],
        "debug_mode": app.config['DEBUG']
    }
    logger.debug(f"Demande de statut : {status_data}")
    return jsonify(status_data)

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 sur {request.path}")
    return jsonify({"error": "Ressource introuvable", "code": 404}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Erreur 500 : {e}")
    return jsonify({"error": "Erreur interne critique", "code": 500}), 500

if __name__ == "__main__":
    logger.info("Démarrage du serveur de développement...")
    app.run()
