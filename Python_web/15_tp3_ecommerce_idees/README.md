# TP3 : E-Commerce "Bonnes Idées & Câlins Virtuels"

## Concept
Une boutique en ligne (un peu absurde) qui vend des bonnes idées et des câlins virtuels.
Monnaie : Neurones 🧠

## Fonctionnalités
- Catalogue produits avec catégories et filtres
- Fiche produit détaillée avec suggestions
- Panier persistant en session
- Mise à jour des quantités
- Checkout avec formulaire validé
- Confirmation de commande
- Historique des commandes (JSON)
- Pages annexes (About, FAQ)

## Installation
```bash
pip install flask
```

## Lancement
```bash
python app.py
```
Puis visiter http://127.0.0.1:5000

## Structure
```
15_tp3_ecommerce_idees/
├── app.py              # Application principale
├── orders.json         # Historique (auto-créé)
├── static/
│   └── css/
│       └── style.css   # Styles
└── templates/
    ├── base.html       # Layout
    ├── index.html      # Accueil
    ├── shop.html       # Boutique
    ├── product.html    # Fiche produit
    ├── cart.html       # Panier
    ├── checkout.html   # Checkout
    ├── confirmation.html
    ├── about.html
    └── faq.html
```

## Produits disponibles
- 💡 Idées (4 variantes)
- 🤗 Câlins virtuels (4 variantes)  
- 🚀 Combos

## Ce que j'ai appris
- Gestion de sessions Flask
- Context processors
- Templates Jinja2 avancés
- Persistance JSON
- Validation côté serveur
- Design responsive
