from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
import uuid
from datetime import datetime
from functools import wraps

# Import configurations and models
from config import config
from models import db, bcrypt, User, Product, Order, OrderItem, Review, Wishlist
from email_utils import mail, send_order_confirmation_email, send_welcome_email, send_password_reset_email
from payment_utils import create_payment_intent, confirm_payment
from forms import LoginForm, RegisterForm, ProductForm, CheckoutForm, ReviewForm
from templates import MAIN_TEMPLATE, ADMIN_DASHBOARD_TEMPLATE
from templates_orders import ORDERS_PAGE_TEMPLATE

app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin required decorator
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database and seed data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@shopeasy.com').first()
        if not admin:
            admin = User(
                email='admin@shopeasy.com',
                username='admin',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Seed products if empty
        if Product.query.count() == 0:
            products = [
                # Electronics Products
                Product(
                    name="Wireless Headphones",
                    description="High-quality wireless headphones with noise cancellation",
                    price=99.99,
                    image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop",
                    category="Electronics",
                    stock=50,
                    rating=4.5,
                    features=["Noise Cancellation", "30hr Battery", "Wireless", "Bluetooth 5.0", "Foldable Design", "Built-in Mic", "Premium Sound"]
                ),
                Product(
                    name="Smart Watch",
                    description="Feature-rich smartwatch with health monitoring",
                    price=199.99,
                    image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop",
                    category="Electronics",
                    stock=30,
                    rating=4.2,
                    features=["Heart Rate Monitor", "GPS", "Water Resistant", "Sleep Tracking", "Fitness Modes", "Notifications", "Long Battery"]
                ),
                Product(
                    name="Laptop",
                    description="Powerful laptop for work and gaming",
                    price=899.99,
                    image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop",
                    category="Electronics",
                    stock=15,
                    rating=4.8,
                    features=["16GB RAM", "512GB SSD", "Intel i7", "15.6 Display", "Backlit Keyboard", "Windows 11", "Lightweight"]
                ),
                Product(
                    name="Wireless Mouse",
                    description="Ergonomic wireless mouse with precision tracking",
                    price=29.99,
                    image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop",
                    category="Electronics",
                    stock=100,
                    rating=4.3,
                    features=["Wireless", "Ergonomic", "Long Battery", "DPI Adjustable", "Silent Click", "USB Receiver"]
                ),
                
                # Fashion Products
                Product(
                    name="Running Shoes",
                    description="Comfortable running shoes for all terrains",
                    price=79.99,
                    image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop",
                    category="Fashion",
                    stock=45,
                    rating=4.7,
                    features=["Lightweight", "Breathable", "Durable", "Cushioned Sole", "Anti-Slip", "Mesh Upper"]
                ),
                Product(
                    name="Backpack",
                    description="Waterproof backpack with laptop compartment",
                    price=39.99,
                    image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop",
                    category="Fashion",
                    stock=40,
                    rating=4.6,
                    features=["Waterproof", "Laptop Sleeve", "Multiple Pockets", "USB Port", "Padded Straps", "30L Capacity"]
                ),
                Product(
                    name="Sunglasses",
                    description="Stylish UV protection sunglasses",
                    price=49.99,
                    image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=300&fit=crop",
                    category="Fashion",
                    stock=60,
                    rating=4.4,
                    features=["UV Protection", "Polarized", "Lightweight", "Scratch Resistant", "Metal Frame", "Case Included"]
                ),
                Product(
                    name="Leather Jacket",
                    description="Premium leather jacket for all seasons",
                    price=149.99,
                    image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop",
                    category="Fashion",
                    stock=20,
                    rating=4.9,
                    features=["Genuine Leather", "Warm", "Stylish", "Multiple Pockets", "Zipper Closure", "Premium Quality"]
                ),
                
                # Home Products
                Product(
                    name="Coffee Maker",
                    description="Automatic coffee maker with timer",
                    price=49.99,
                    image_url="https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400&h=300&fit=crop",
                    category="Home",
                    stock=25,
                    rating=4.3,
                    features=["24hr Timer", "Auto Shut-off", "Programmable", "12 Cup Capacity", "Keep Warm", "Easy Clean"]
                ),
                Product(
                    name="Desk Lamp",
                    description="LED desk lamp with adjustable brightness",
                    price=29.99,
                    image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop",
                    category="Home",
                    stock=60,
                    rating=4.4,
                    features=["Adjustable Brightness", "USB Port", "Modern Design", "Touch Control", "Eye Protection", "Energy Saving"]
                ),
                Product(
                    name="Wall Clock",
                    description="Modern minimalist wall clock",
                    price=24.99,
                    image_url="https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400&h=300&fit=crop",
                    category="Home",
                    stock=35,
                    rating=4.2,
                    features=["Silent Movement", "Modern Design", "Easy to Read", "Battery Operated", "12 Inch", "Wall Mount"]
                ),
                Product(
                    name="Plant Pot Set",
                    description="Set of 3 ceramic plant pots",
                    price=19.99,
                    image_url="https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400&h=300&fit=crop",
                    category="Home",
                    stock=50,
                    rating=4.5,
                    features=["Ceramic", "Drainage Holes", "Set of 3", "Different Sizes", "Indoor/Outdoor", "Decorative"]
                ),
                
                # Sports Products
                Product(
                    name="Yoga Mat",
                    description="Non-slip yoga mat with carrying strap",
                    price=34.99,
                    image_url="https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop",
                    category="Sports",
                    stock=70,
                    rating=4.6,
                    features=["Non-slip", "Eco-friendly", "6mm Thick", "Carrying Strap", "Easy Clean", "Durable Material"]
                ),
                Product(
                    name="Dumbbell Set",
                    description="Adjustable dumbbell set for home workout",
                    price=89.99,
                    image_url="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop",
                    category="Sports",
                    stock=30,
                    rating=4.7,
                    features=["Adjustable Weight", "Compact", "Durable", "5-25 lbs Range", "Anti-Roll Design", "Rubber Coated"]
                ),
                Product(
                    name="Water Bottle",
                    description="Insulated stainless steel water bottle",
                    price=19.99,
                    image_url="https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=300&fit=crop",
                    category="Sports",
                    stock=100,
                    rating=4.5,
                    features=["Insulated", "BPA Free", "750ml", "Leak Proof", "24hr Cold", "Stainless Steel"]
                ),
                
                # Books Products
                Product(
                    name="Python Programming Book",
                    description="Complete guide to Python programming",
                    price=39.99,
                    image_url="https://images.unsplash.com/photo-1589998059171-988d887df646?w=400&h=300&fit=crop",
                    category="Books",
                    stock=50,
                    rating=4.8,
                    features=["Beginner Friendly", "500 Pages", "Code Examples", "Exercises", "Hardcover", "Latest Edition"]
                ),
                Product(
                    name="Business Strategy Book",
                    description="Essential business strategies for success",
                    price=29.99,
                    image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop",
                    category="Books",
                    stock=40,
                    rating=4.6,
                    features=["Best Seller", "Case Studies", "Practical Tips", "300 Pages", "Paperback", "Expert Author"]
                ),
                Product(
                    name="Cookbook Collection",
                    description="Delicious recipes from around the world",
                    price=34.99,
                    image_url="https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=400&h=300&fit=crop",
                    category="Books",
                    stock=35,
                    rating=4.7,
                    features=["200+ Recipes", "Full Color", "Step by Step", "Nutritional Info", "Hardcover", "Illustrated"]
                ),
                
                # Toys Products
                Product(
                    name="Building Blocks Set",
                    description="Creative building blocks for kids",
                    price=44.99,
                    image_url="https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400&h=300&fit=crop",
                    category="Toys",
                    stock=60,
                    rating=4.9,
                    features=["500 Pieces", "Safe Materials", "Age 3+", "Educational", "Storage Box", "Multiple Colors"]
                ),
                Product(
                    name="Remote Control Car",
                    description="High-speed RC car with rechargeable battery",
                    price=59.99,
                    image_url="https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?w=400&h=300&fit=crop",
                    category="Toys",
                    stock=45,
                    rating=4.5,
                    features=["High Speed", "Rechargeable", "Remote Control", "Durable", "LED Lights", "Age 6+"]
                ),
                Product(
                    name="Puzzle Game",
                    description="Challenging 1000-piece jigsaw puzzle",
                    price=24.99,
                    image_url="https://images.unsplash.com/photo-1611604548018-d56bbd85d681?w=400&h=300&fit=crop",
                    category="Toys",
                    stock=55,
                    rating=4.4,
                    features=["1000 Pieces", "Beautiful Art", "Premium Quality", "Age 8+", "Gift Box", "Poster Included"]
                )
            ]
            db.session.add_all(products)
        
        db.session.commit()
        print("Database initialized successfully!")

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/register', methods=['POST'])
def register():
    """User registration"""
    data = request.get_json()
    
    # Validate input
    if not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Username already taken'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        username=data['username']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Send welcome email
    send_welcome_email(user, app)
    
    # Log user in
    login_user(user)
    
    return jsonify({
        'success': True,
        'message': 'Registration successful!',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'is_admin': user.is_admin
        }
    })

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_admin': user.is_admin
            }
        })
    
    return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """User logout"""
    logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/current-user')
def get_current_user():
    """Get current logged-in user"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'username': current_user.username,
                'is_admin': current_user.is_admin
            }
        })
    return jsonify({'authenticated': False})

# ==================== PRODUCT ROUTES ====================

@app.route('/api/products')
def get_products():
    """Get all products"""
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'image': p.image_url,
        'category': p.category,
        'stock': p.stock,
        'inStock': p.in_stock,
        'rating': p.rating,
        'features': p.features or []
    } for p in products])

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    """Get single product"""
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image': product.image_url,
        'category': product.category,
        'stock': product.stock,
        'inStock': product.in_stock,
        'rating': product.rating,
        'features': product.features or [],
        'reviews': [{
            'id': r.id,
            'user': r.user.username,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d')
        } for r in product.reviews]
    })

# ==================== CART ROUTES ====================

@app.route('/api/cart')
def get_cart():
    """Get cart items"""
    cart = session.get('cart', [])
    return jsonify(cart)

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    product = Product.query.get_or_404(product_id)
    
    if not product.in_stock:
        return jsonify({'success': False, 'message': 'Product out of stock'}), 400
    
    cart = session.get('cart', [])
    
    # Check if product already in cart
    cart_item = next((item for item in cart if item['id'] == product_id), None)
    
    if cart_item:
        if cart_item['quantity'] < product.stock:
            cart_item['quantity'] += 1
        else:
            return jsonify({'success': False, 'message': 'Not enough stock'}), 400
    else:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': product.image_url,
            'quantity': 1
        })
    
    session['cart'] = cart
    return jsonify({'success': True, 'cart': cart})

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    
    session['cart'] = cart
    return jsonify({'success': True, 'cart': cart})

@app.route('/api/cart/update', methods=['POST'])
def update_cart_quantity():
    """Update cart item quantity"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    product = Product.query.get_or_404(product_id)
    
    if quantity > product.stock:
        return jsonify({'success': False, 'message': 'Not enough stock'}), 400
    
    cart = session.get('cart', [])
    cart_item = next((item for item in cart if item['id'] == product_id), None)
    
    if cart_item:
        if quantity <= 0:
            cart = [item for item in cart if item['id'] != product_id]
        else:
            cart_item['quantity'] = quantity
    
    session['cart'] = cart
    return jsonify({'success': True, 'cart': cart})

# ==================== WISHLIST ROUTES ====================

@app.route('/api/wishlist')
@login_required
def get_wishlist():
    """Get user wishlist"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': item.product.id,
        'name': item.product.name,
        'price': item.product.price,
        'image': item.product.image_url,
        'inStock': item.product.in_stock
    } for item in wishlist_items])

@app.route('/api/wishlist/toggle', methods=['POST'])
@login_required
def toggle_wishlist():
    """Add/remove item from wishlist"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    product = Product.query.get_or_404(product_id)
    
    wishlist_item = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        message = 'Removed from wishlist'
    else:
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        message = 'Added to wishlist'
    
    wishlist = Wishlist.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'success': True,
        'message': message,
        'wishlist': [{
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'image': item.product.image_url,
            'inStock': item.product.in_stock
        } for item in wishlist]
    })

@app.route('/api/wishlist/clear', methods=['POST'])
@login_required
def clear_wishlist():
    """Clear user wishlist"""
    Wishlist.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Wishlist cleared'})


# ==================== CHECKOUT & ORDER ROUTES ====================

@app.route('/api/checkout', methods=['POST'])
@login_required
def checkout():
    """Process checkout"""
    data = request.get_json()
    cart = session.get('cart', [])
    
    if not cart:
        return jsonify({'success': False, 'message': 'Cart is empty'}), 400
    
    # Validate shipping details
    required_fields = ['shipping_name', 'shipping_email', 'shipping_address', 
                      'shipping_city', 'shipping_state', 'shipping_zip', 
                      'shipping_country', 'shipping_phone']
    
    for field in required_fields:
        if not data.get(field):
            return jsonify({'success': False, 'message': f'{field} is required'}), 400
    
    # Calculate total
    total_amount = sum(item['price'] * item['quantity'] for item in cart)
    
    # Create payment intent (OPTIONAL - Skip if Stripe not configured)
    payment_id = None
    try:
        if app.config.get('STRIPE_SECRET_KEY'):
            payment_intent = create_payment_intent(
                amount=total_amount,
                metadata={
                    'user_id': current_user.id,
                    'user_email': current_user.email
                }
            )
            if payment_intent:
                payment_id = payment_intent.id
    except Exception as e:
        print(f"Stripe payment skipped: {e}")
        # Continue without payment - for testing
    
    # Create order
    order = Order(
        order_number=f'ORD-{uuid.uuid4().hex[:8].upper()}',
        user_id=current_user.id,
        total_amount=total_amount,
        status='confirmed',  # Auto-confirm for testing
        payment_status='completed',  # Auto-complete for testing
        payment_id=payment_id or f'TEST-{uuid.uuid4().hex[:8]}',
        shipping_name=data['shipping_name'],
        shipping_email=data['shipping_email'],
        shipping_address=data['shipping_address'],
        shipping_city=data['shipping_city'],
        shipping_state=data['shipping_state'],
        shipping_zip=data['shipping_zip'],
        shipping_country=data['shipping_country'],
        shipping_phone=data['shipping_phone']
    )
    
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Create order items and update stock
    for item in cart:
        product = Product.query.get(item['id'])
        if product.stock < item['quantity']:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Not enough stock for {product.name}'}), 400
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item['quantity'],
            price=product.price
        )
        db.session.add(order_item)
        
        # Update stock
        product.stock -= item['quantity']
    
    db.session.commit()
    
    # Clear cart
    session['cart'] = []
    
    # Send confirmation email (OPTIONAL - Skip if email not configured)
    try:
        if app.config.get('MAIL_USERNAME'):
            send_order_confirmation_email(order, app)
    except Exception as e:
        print(f"Email sending skipped: {e}")
    
    return jsonify({
        'success': True,
        'message': 'Order placed successfully!',
        'order_number': order.order_number,
        'payment_client_secret': 'test_secret_for_demo'
    })

@app.route('/api/orders')
@login_required
def get_orders():
    """Get user orders"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': order.id,
        'order_number': order.order_number,
        'total_amount': order.total_amount,
        'status': order.status,
        'payment_status': order.payment_status,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
        'items': [{
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.items]
    } for order in orders])

@app.route('/api/orders/<int:order_id>')
@login_required
def get_order(order_id):
    """Get single order details"""
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order
    if order.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    return jsonify({
        'id': order.id,
        'order_number': order.order_number,
        'total_amount': order.total_amount,
        'status': order.status,
        'payment_status': order.payment_status,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
        'shipping': {
            'name': order.shipping_name,
            'email': order.shipping_email,
            'address': order.shipping_address,
            'city': order.shipping_city,
            'state': order.shipping_state,
            'zip': order.shipping_zip,
            'country': order.shipping_country,
            'phone': order.shipping_phone
        },
        'items': [{
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_image': item.product.image_url,
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': item.price * item.quantity
        } for item in order.items]
    })

# ==================== REVIEW ROUTES ====================

@app.route('/api/reviews/<int:product_id>')
def get_product_reviews(product_id):
    """Get reviews for a product"""
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return jsonify([{
        'id': review.id,
        'user': review.user.username,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at.strftime('%Y-%m-%d')
    } for review in reviews])

@app.route('/api/reviews/add', methods=['POST'])
@login_required
def add_review():
    """Add product review"""
    data = request.get_json()
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment', '')
    
    if not product_id or not rating:
        return jsonify({'success': False, 'message': 'Product ID and rating required'}), 400
    
    if rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
    
    product = Product.query.get_or_404(product_id)
    
    # Check if user already reviewed this product
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if existing_review:
        return jsonify({'success': False, 'message': 'You already reviewed this product'}), 400
    
    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(review)
    product.update_rating()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Review added successfully',
        'review': {
            'id': review.id,
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime('%Y-%m-%d')
        }
    })

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.payment_status == 'completed'
    ).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template_string(ADMIN_DASHBOARD_TEMPLATE, 
                                 total_users=total_users,
                                 total_products=total_products,
                                 total_orders=total_orders,
                                 total_revenue=total_revenue,
                                 recent_orders=recent_orders)

@app.route('/api/admin/products', methods=['GET', 'POST'])
@admin_required
def admin_products():
    """Admin product management"""
    if request.method == 'POST':
        data = request.get_json()
        
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            image_url=data.get('image_url', ''),
            category=data.get('category', 'Other'),
            stock=int(data.get('stock', 0)),
            features=data.get('features', '').split(',') if data.get('features') else []
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Product added successfully', 'product_id': product.id})
    
    # GET request
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'image_url': p.image_url,
        'category': p.category,
        'stock': p.stock,
        'rating': p.rating
    } for p in products])

@app.route('/api/admin/products/<int:product_id>', methods=['PUT', 'DELETE'])
@admin_required
def admin_product_detail(product_id):
    """Update or delete product"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    
    # PUT request
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = float(data.get('price', product.price))
    product.image_url = data.get('image_url', product.image_url)
    product.category = data.get('category', product.category)
    product.stock = int(data.get('stock', product.stock))
    
    if data.get('features'):
        product.features = data['features'].split(',') if isinstance(data['features'], str) else data['features']
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Product updated successfully'})

@app.route('/api/admin/orders')
@admin_required
def admin_orders():
    """Get all orders for admin"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': order.id,
        'order_number': order.order_number,
        'user_email': order.user.email,
        'total_amount': order.total_amount,
        'status': order.status,
        'payment_status': order.payment_status,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M')
    } for order in orders])

@app.route('/api/admin/orders/<int:order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    new_status = data.get('status')
    if new_status not in ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    order.status = new_status
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Order status updated'})

@app.route('/api/admin/users')
@admin_required
def admin_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.strftime('%Y-%m-%d'),
        'total_orders': len(user.orders)
    } for user in users])

# ==================== MAIN ROUTE ====================

@app.route('/')
def home():
    """Main application page"""
    products = Product.query.all()
    return render_template_string(MAIN_TEMPLATE, products=products)

@app.route('/orders')
@login_required
def orders_page():
    """User orders page"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template_string(ORDERS_PAGE_TEMPLATE, orders=orders)



if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run application
    app.run(host='0.0.0.0', port=5000, debug=True)
