import os

# 22/11/2023 - Geoffroy
# Configuration externalisée.
# On ne garde pas ses secrets dans sa poche, on les met dans un coffre.

class Config:
    DEBUG = False
    TESTING = False
    SERVER_NAME = "127.0.0.1:5000"

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    # Pour plus tard... quand on sortira du tuto.
    pass
