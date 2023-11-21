import flask
import sys
import platform

# 21/11/2023 - Geoffroy
# Update : Ajout de quelques détails sur le système.
# C'est toujours bon de savoir sur quel terrain on évolue (OS, version Python...).
# Comme vérifier la météo avant de sortir de l'auberge.

def check_installation():
    print(f"--- Rapport de reconnaissance ---")
    print(f"Système      : {platform.system()} {platform.release()}")
    print(f"Python       : {sys.version.split()[0]}")
    print(f"Flask        : {flask.__version__}")
    print("---------------------------------")
    print("Moteur démarré. Le 'Dungeon Master' Python est prêt.")

if __name__ == "__main__":
    check_installation()
