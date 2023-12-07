from flask import Flask, render_template, session, redirect, url_for, request, flash
from functools import wraps
import secrets
import json
from datetime import datetime
import os

# ============================================
# 07/12/2023 - Geoffroy
# TP3 : E-Commerce "Bonnes Idées & Câlins Virtuels"
# ============================================
# 
# Bon, j'avoue, l'idée est un peu absurde. Mais c'est le but.
# Qui n'a jamais voulu acheter une bonne idée sur Internet ?
# Et les câlins virtuels, c'est l'avenir du bien-être digital.
# 
# Ce projet combine tout ce que j'ai appris :
# - Sessions (panier)
# - Templates (beaucoup)
# - Formulaires (checkout)
# - Persistance JSON (commandes)
# 
# Note pour mon moi du futur : oui, les prix sont en "neurones".
# C'est la monnaie officielle des bonnes idées.
# 
# TODO: Ajouter un système de fidélité basé sur le karma
# TODO: Intégrer un générateur d'idées aléatoires (IA ?)
# ============================================

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Chemins pour la persistance
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')

# ============================================
# CATALOGUE DE PRODUITS
# Oui, on vend vraiment ça. Non, je ne suis pas fou.
# (enfin, peut-être un peu)
# ============================================

PRODUCTS = {
    # Les Bonnes Idées (notre bestseller)
    "idea_001": {
        "id": "idea_001",
        "name": "Idée de Génie (Garantie 24h)",
        "description": "Une idée brillante livrée directement dans votre cerveau. Attention : peut provoquer des 'Eureka!' intempestifs.",
        "price": 99,
        "category": "ideas",
        "stock": 42,  # Évidemment
        "emoji": "💡",
        "reviews": 4.8
    },
    "idea_002": {
        "id": "idea_002",
        "name": "Idée Moyenne (mais honnête)",
        "description": "Pas révolutionnaire, mais ça fait le job. Parfait pour les réunions du lundi matin.",
        "price": 29,
        "category": "ideas",
        "stock": 156,
        "emoji": "🤔",
        "reviews": 3.5
    },
    "idea_003": {
        "id": "idea_003",
        "name": "Pack 'Brainstorm' (5 idées)",
        "description": "Cinq idées en vrac. Qualité variable. Peut contenir des traces de nonsense.",
        "price": 149,
        "category": "ideas",
        "stock": 23,
        "emoji": "🧠",
        "reviews": 4.2
    },
    "idea_004": {
        "id": "idea_004", 
        "name": "Idée Vintage (années 90)",
        "description": "Une idée rétro qui a fait ses preuves. Sent légèrement le Tamagotchi.",
        "price": 45,
        "category": "ideas",
        "stock": 12,
        "emoji": "📼",
        "reviews": 4.0
    },
    
    # Les Câlins Virtuels (notre département bien-être)
    "hug_001": {
        "id": "hug_001",
        "name": "Câlin Standard (v2.3)",
        "description": "Un câlin virtuel de base. Chaleur émotionnelle garantie. Compatible tous navigateurs.",
        "price": 15,
        "category": "hugs",
        "stock": 9999,  # Illimité, c'est virtuel après tout
        "emoji": "🤗",
        "reviews": 4.9
    },
    "hug_002": {
        "id": "hug_002",
        "name": "Câlin Premium (avec petits coeurs)",
        "description": "Version deluxe. Inclut des petits coeurs flottants et un fond sonore apaisant.",
        "price": 35,
        "category": "hugs",
        "stock": 500,
        "emoji": "💝",
        "reviews": 5.0
    },
    "hug_003": {
        "id": "hug_003",
        "name": "Câlin d'Ours Polaire",
        "description": "Extra chaud. Recommandé pour les lundis difficiles et les ruptures Tinder.",
        "price": 55,
        "category": "hugs",
        "stock": 78,
        "emoji": "🐻‍❄️",
        "reviews": 4.7
    },
    "hug_004": {
        "id": "hug_004",
        "name": "Abonnement Câlins Illimités (1 mois)",
        "description": "Tous les câlins que vous voulez pendant 30 jours. Usage personnel uniquement.",
        "price": 199,
        "category": "hugs",
        "stock": 50,
        "emoji": "♾️",
        "reviews": 4.6
    },
    
    # Les Combos (parce que les gens aiment les promos)
    "combo_001": {
        "id": "combo_001",
        "name": "Combo Startup (1 idée + 3 câlins)",
        "description": "Tout ce qu'il faut pour lancer votre projet. L'idée pour pitcher, les câlins pour les refus.",
        "price": 129,
        "category": "combos",
        "stock": 30,
        "emoji": "🚀",
        "reviews": 4.4
    }
}

# ============================================
# HELPERS
# (les petites fonctions qui font le boulot)
# ============================================

def get_cart():
    """Récupère le panier depuis la session. Simple comme bonjour."""
    return session.get('cart', {})

def save_cart(cart):
    """Sauvegarde le panier. Révolutionnaire, je sais."""
    session['cart'] = cart

def get_cart_total():
    """Calcule le total du panier. Maths niveau CE2."""
    cart = get_cart()
    total = 0
    for product_id, quantity in cart.items():
        if product_id in PRODUCTS:
            total += PRODUCTS[product_id]['price'] * quantity
    return total

def get_cart_count():
    """Compte les articles. Pour le badge du panier."""
    return sum(get_cart().values())

def load_orders():
    """Charge l'historique des commandes depuis le JSON."""
    if not os.path.exists(ORDERS_FILE):
        return []
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_order(order):
    """Sauvegarde une nouvelle commande."""
    orders = load_orders()
    orders.append(order)
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)

# Injecte le compteur de panier dans tous les templates
# (merci Flask pour ce context processor)
@app.context_processor
def inject_cart_count():
    return {'cart_count': get_cart_count()}

# ============================================
# ROUTES - LA BOUTIQUE
# ============================================

@app.route('/')
def index():
    """Page d'accueil. La vitrine de notre empire de bonnes idées."""
    # Produits vedettes (les mieux notés)
    featured = sorted(PRODUCTS.values(), key=lambda x: x['reviews'], reverse=True)[:4]
    return render_template('index.html', featured=featured)

@app.route('/shop')
@app.route('/shop/<category>')
def shop(category=None):
    """La boutique. Où la magie opère."""
    products = list(PRODUCTS.values())
    
    if category:
        products = [p for p in products if p['category'] == category]
    
    # Tri par prix (croissant par défaut)
    sort_by = request.args.get('sort', 'price')
    if sort_by == 'price':
        products.sort(key=lambda x: x['price'])
    elif sort_by == 'reviews':
        products.sort(key=lambda x: x['reviews'], reverse=True)
    elif sort_by == 'name':
        products.sort(key=lambda x: x['name'])
    
    return render_template('shop.html', 
        products=products, 
        current_category=category,
        current_sort=sort_by
    )

@app.route('/product/<product_id>')
def product_detail(product_id):
    """Fiche produit. Pour les indécis qui veulent plus de détails."""
    product = PRODUCTS.get(product_id)
    if not product:
        flash("Produit introuvable. Peut-être qu'il s'est envolé ? 🦋", "error")
        return redirect(url_for('shop'))
    
    # Suggestions (même catégorie, exclure le produit actuel)
    suggestions = [p for p in PRODUCTS.values() 
                   if p['category'] == product['category'] and p['id'] != product_id][:3]
    
    return render_template('product.html', product=product, suggestions=suggestions)

# ============================================
# ROUTES - LE PANIER
# ============================================

@app.route('/cart')
def cart():
    """Le panier. Là où vos bonnes décisions s'accumulent."""
    cart_items = []
    cart_data = get_cart()
    
    for product_id, quantity in cart_data.items():
        if product_id in PRODUCTS:
            item = PRODUCTS[product_id].copy()
            item['quantity'] = quantity
            item['subtotal'] = item['price'] * quantity
            cart_items.append(item)
    
    return render_template('cart.html', 
        items=cart_items, 
        total=get_cart_total()
    )

@app.route('/cart/add/<product_id>')
def cart_add(product_id):
    """Ajoute un produit au panier. Clic, c'est fait."""
    if product_id not in PRODUCTS:
        flash("Ce produit n'existe pas. Tentative de fraude ? 🤨", "error")
        return redirect(url_for('shop'))
    
    product = PRODUCTS[product_id]
    cart = get_cart()
    
    # Vérifier le stock (même si pour les câlins virtuels c'est absurde)
    current_qty = cart.get(product_id, 0)
    if current_qty >= product['stock']:
        flash(f"Stock insuffisant ! On ne peut pas inventer plus de {product['name']}.", "error")
        return redirect(url_for('shop'))
    
    cart[product_id] = current_qty + 1
    save_cart(cart)
    
    flash(f"✅ {product['emoji']} {product['name']} ajouté au panier !", "success")
    
    # Retour à la page précédente ou à la boutique
    return redirect(request.referrer or url_for('shop'))

@app.route('/cart/remove/<product_id>')
def cart_remove(product_id):
    """Retire un produit du panier. Snif."""
    cart = get_cart()
    
    if product_id in cart:
        del cart[product_id]
        save_cart(cart)
        flash("Produit retiré. On ne vous en veut pas. 😢", "info")
    
    return redirect(url_for('cart'))

@app.route('/cart/update', methods=['POST'])
def cart_update():
    """Met à jour les quantités. Pour les perfectionnistes."""
    cart = get_cart()
    
    for product_id in cart.keys():
        new_qty = request.form.get(f'qty_{product_id}', type=int)
        if new_qty is not None:
            if new_qty <= 0:
                del cart[product_id]
            else:
                max_stock = PRODUCTS[product_id]['stock']
                cart[product_id] = min(new_qty, max_stock)
    
    save_cart(cart)
    flash("Panier mis à jour ! 🛒", "success")
    return redirect(url_for('cart'))

@app.route('/cart/clear')
def cart_clear():
    """Vide le panier. Le bouton nucléaire."""
    session.pop('cart', None)
    flash("Panier vidé. Tabula rasa. 🧹", "info")
    return redirect(url_for('shop'))

# ============================================
# ROUTES - CHECKOUT
# ============================================

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Le checkout. L'heure de vérité."""
    cart = get_cart()
    
    if not cart:
        flash("Votre panier est vide ! Allez faire du shopping d'abord. 🛍️", "error")
        return redirect(url_for('shop'))
    
    if request.method == 'POST':
        # Récupération des infos client
        # (dans un vrai site, on validerait tout ça sérieusement)
        customer = {
            "name": request.form.get('name', '').strip(),
            "email": request.form.get('email', '').strip(),
            "brain_address": request.form.get('brain_address', '').strip(),  # Pour la livraison mentale
        }
        
        # Validation basique (très basique, on est dimanche)
        errors = []
        if len(customer['name']) < 2:
            errors.append("Le nom doit faire au moins 2 caractères. Même 'Jo' compte.")
        if '@' not in customer['email']:
            errors.append("L'email semble invalide. On a besoin d'un @ quelque part.")
        if not customer['brain_address']:
            errors.append("L'adresse mentale est requise pour la livraison d'idées.")
        
        if errors:
            for error in errors:
                flash(f"❌ {error}", "error")
            return render_template('checkout.html', 
                cart=get_cart(),
                total=get_cart_total(),
                customer=customer
            )
        
        # Créer la commande
        order = {
            "id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "date": datetime.now().isoformat(),
            "customer": customer,
            "items": [],
            "total": get_cart_total(),
            "status": "confirmed",
            "payment_method": "neurones"  # La seule monnaie acceptée
        }
        
        for product_id, quantity in cart.items():
            if product_id in PRODUCTS:
                product = PRODUCTS[product_id]
                order['items'].append({
                    "product_id": product_id,
                    "name": product['name'],
                    "price": product['price'],
                    "quantity": quantity,
                    "subtotal": product['price'] * quantity
                })
        
        # Sauvegarder et vider le panier
        save_order(order)
        session.pop('cart', None)
        session['last_order'] = order['id']
        
        return redirect(url_for('order_confirmation'))
    
    return render_template('checkout.html', 
        cart=get_cart(),
        total=get_cart_total(),
        customer={}
    )

@app.route('/order/confirmation')
def order_confirmation():
    """Page de confirmation. Le moment de dopamine."""
    order_id = session.get('last_order')
    if not order_id:
        return redirect(url_for('index'))
    
    # Récupérer la commande
    orders = load_orders()
    order = next((o for o in orders if o['id'] == order_id), None)
    
    return render_template('confirmation.html', order=order)

# ============================================
# ROUTES - PAGES ANNEXES
# ============================================

@app.route('/about')
def about():
    """À propos. L'histoire derrière cette folie."""
    return render_template('about.html')

@app.route('/faq')
def faq():
    """FAQ. Parce qu'on sait que vous avez des questions."""
    return render_template('faq.html')

# ============================================
# GESTION DES ERREURS
# ============================================

@app.errorhandler(404)
def not_found(e):
    flash("Page introuvable. Comme une bonne idée un lundi matin. 🤷", "error")
    return redirect(url_for('index'))

# ============================================
# LANCEMENT
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("🛒 Boutique 'Bonnes Idées & Câlins Virtuels'")
    print("📍 http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
