#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# 28/11/2023 - Geoffroy
# Django V2 - Structure plus professionnelle
# J'ai réorganisé et ajouté des logs au démarrage.
# C'est toujours bien de savoir ce qui se passe au boot.

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Log de démarrage
    print("=" * 50)
    print("🐍 Django Management Tool")
    print(f"📂 Settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print("=" * 50)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Vérifiez:\n"
            "1. Django est-il installé? (pip install django)\n"
            "2. L'environnement virtuel est-il activé?\n"
            "3. PYTHONPATH est-il correctement configuré?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
