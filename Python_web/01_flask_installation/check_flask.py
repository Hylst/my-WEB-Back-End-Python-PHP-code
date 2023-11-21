import flask

# 21/11/2023 - Geoffroy
# Premier jet pour vérifier que l'équipement est prêt.
# C'est un peu comme vérifier sa fiche de perso avant le début de la campagne.
# Si Flask répond présent, on peut partir à l'aventure.

def check_installation():
    print(f"Flask version: {flask.__version__}")
    print("Moteur démarré. Le 'Dungeon Master' Python est prêt.")

if __name__ == "__main__":
    check_installation()
