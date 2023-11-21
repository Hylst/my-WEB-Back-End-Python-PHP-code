import flask
import sys
import platform
import os
import shutil

# 21/11/2023 - Geoffroy
# Update Soirée : J'ai creusé un peu plus.
# Un bon aventurier vérifie toujours son inventaire ET son environnement.
# Ce script scanne tout : version, environnement virtuel, espace disque...
# C'est peut-être overkill, mais j'aime bien savoir où je mets les pieds.

def check_system():
    print(f"\n--- [ SCAN SYSTÈME ] ---")
    print(f"OS           : {platform.system()} {platform.release()} ({platform.version()})")
    print(f"Machine      : {platform.machine()}")
    print(f"Processeur   : {platform.processor()}")
    
    # Check disque pour éviter les surprises
    total, used, free = shutil.disk_usage(".")
    print(f"Espace Disque: {free // (2**30)} Go libres / {total // (2**30)} Go total")

def check_python_env():
    print(f"\n--- [ ENVIRONNEMENT PYTHON ] ---")
    print(f"Version      : {sys.version.split()[0]}")
    print(f"Exécutable   : {sys.executable}")
    
    # Vérification VENV
    in_venv = (sys.prefix != sys.base_prefix)
    status = "ACTIVÉ ✅" if in_venv else "DÉSACTIVÉ ⚠️ (Attention aux conflits)"
    print(f"Virtual Env  : {status}")
    
    # Path
    print(f"PYTHONPATH   : {os.environ.get('PYTHONPATH', 'Non défini')}")

def check_flask():
    print(f"\n--- [ MODULE FLASK ] ---")
    try:
        print(f"Version      : {flask.__version__}")
        print(f"Chemin       : {os.path.dirname(flask.__file__)}")
        print("Statut       : OPÉRATIONNEL 🚀")
    except Exception as e:
        print(f"Statut       : ERREUR CRITIQUE 💀 ({e})")

if __name__ == "__main__":
    print("Initialisation des protocoles de diagnostic...")
    check_system()
    check_python_env()
    check_flask()
    print("\n[ FIN DU RAPPORT ]")
