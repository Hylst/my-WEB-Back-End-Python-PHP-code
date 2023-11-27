from flask import Flask, session, redirect, url_for, render_template_string, request
import secrets

# 27/11/2023 - Geoffroy
# Sessions V2 - Panier d'achats simulé
# Au lieu d'un simple compteur, on gère un vrai panier avec ajout/suppression.
# Ça montre mieux la puissance des sessions pour stocker des structures complexes.

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Catalogue de produits simulé
PRODUCTS = {
    1: {"name": "Épée de Feu", "price": 150, "emoji": "⚔️"},
    2: {"name": "Bouclier Runique", "price": 120, "emoji": "🛡️"},
    3: {"name": "Potion de Mana", "price": 25, "emoji": "🧪"},
    4: {"name": "Parchemin Magique", "price": 45, "emoji": "📜"},
    5: {"name": "Anneau de Protection", "price": 200, "emoji": "💍"}
}

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Boutique de la Guilde</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: #eee; }
        .products { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }
        .product { background: #16213e; padding: 15px; border-radius: 8px; text-align: center; }
        .product h3 { margin: 0 0 10px; }
        .emoji { font-size: 2rem; }
        .price { color: #ffd700; font-weight: bold; }
        .cart { background: #0f3460; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .cart-item { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #333; }
        a { color: #4cc9f0; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .btn { display: inline-block; padding: 5px 15px; background: #e94560; color: white; border-radius: 4px; margin-top: 5px; }
        .btn-add { background: #4cc9f0; }
        .total { font-size: 1.2rem; color: #ffd700; margin-top: 15px; }
    </style>
</head>
<body>
    <h1>🏪 Boutique de la Guilde</h1>
    
    <h2>Catalogue</h2>
    <div class="products">
        {% for id, product in products.items() %}
        <div class="product">
            <div class="emoji">{{ product.emoji }}</div>
            <h3>{{ product.name }}</h3>
            <p class="price">{{ product.price }} pièces d'or</p>
            <a href="/add/{{ id }}" class="btn btn-add">Ajouter</a>
        </div>
        {% endfor %}
    </div>
    
    <div class="cart">
        <h2>🛒 Votre Panier ({{ cart|length }} articles)</h2>
        {% if cart %}
            {% for item in cart %}
            <div class="cart-item">
                <span>{{ item.emoji }} {{ item.name }}</span>
                <span>{{ item.price }} po <a href="/remove/{{ loop.index0 }}">[X]</a></span>
            </div>
            {% endfor %}
            <div class="total">Total: {{ total }} pièces d'or</div>
            <p><a href="/clear" class="btn">Vider le panier</a></p>
        {% else %}
            <p>Votre sac est vide...</p>
        {% endif %}
    </div>
    
    <p style="margin-top: 20px; font-size: 0.8rem; color: #666;">
        Session ID: {{ session_id[:8] }}... | 
        <a href="/debug">Debug Session</a>
    </p>
</body>
</html>
"""

@app.route('/')
def shop():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template_string(TEMPLATE, 
        products=PRODUCTS, 
        cart=cart, 
        total=total,
        session_id=session.get('_id', 'N/A')
    )

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    if product_id in PRODUCTS:
        cart = session.get('cart', [])
        cart.append(PRODUCTS[product_id])
        session['cart'] = cart
    return redirect(url_for('shop'))

@app.route('/remove/<int:index>')
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session['cart'] = cart
    return redirect(url_for('shop'))

@app.route('/clear')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('shop'))

@app.route('/debug')
def debug_session():
    return f"<pre>Session: {dict(session)}</pre><p><a href='/'>Retour</a></p>"

if __name__ == "__main__":
    app.run(debug=True)
