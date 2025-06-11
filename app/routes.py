from flask import Blueprint, request, jsonify, abort, render_template, flash, redirect, url_for
from .models import Category, Product
from . import db
from sqlalchemy import func

# Blueprint para la API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Blueprint para la interfaz web
main_bp = Blueprint('main', __name__)

# --- Rutas de la API ---

@api_bp.route('/categories', methods=['GET'])
def list_categories():
    cats = Category.query.all()
    return jsonify([c.to_dict() for c in cats])

@api_bp.route('/categories/<int:cat_id>', methods=['GET'])
def get_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    return jsonify(cat.to_dict())

@api_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    if not data.get('name'):
        abort(400, 'El campo "name" es obligatorio')
    cat = Category(name=data['name'], description=data.get('description'))
    db.session.add(cat); db.session.commit()
    return jsonify(cat.to_dict()), 201

@api_bp.route('/categories/<int:cat_id>', methods=['PUT', 'PATCH'])
def update_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    data = request.get_json() or {}
    cat.name = data.get('name', cat.name)
    cat.description = data.get('description', cat.description)
    db.session.commit()
    return jsonify(cat.to_dict())

@api_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat); db.session.commit()
    return '', 204

@api_bp.route('/products', methods=['GET'])
def list_products():
    prods = Product.query.order_by(Product.created_at.desc()).all()
    return jsonify([p.to_dict() for p in prods])

@api_bp.route('/products/<int:prod_id>', methods=['GET'])
def get_product(prod_id):
    prod = Product.query.get_or_404(prod_id)
    return jsonify(prod.to_dict())

@api_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}
    for field in ('sku','name','price','stock','category_id'):
        if field not in data:
            abort(400, f'Falta el campo "{field}"')
    prod = Product(
        sku=data['sku'],
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        stock=data['stock'],
        category_id=data['category_id']
    )
    db.session.add(prod); db.session.commit()
    return jsonify(prod.to_dict()), 201

@api_bp.route('/products/<int:prod_id>', methods=['PUT','PATCH'])
def update_product(prod_id):
    prod = Product.query.get_or_404(prod_id)
    data = request.get_json() or {}
    prod.sku = data.get('sku', prod.sku)
    prod.name = data.get('name', prod.name)
    prod.description = data.get('description', prod.description)
    prod.price = data.get('price', prod.price)
    prod.stock = data.get('stock', prod.stock)
    prod.category_id = data.get('category_id', prod.category_id)
    db.session.commit()
    return jsonify(prod.to_dict())

@api_bp.route('/products/<int:prod_id>', methods=['DELETE'])
def delete_product(prod_id):
    prod = Product.query.get_or_404(prod_id)
    db.session.delete(prod); db.session.commit()
    return '', 204

# --- Rutas de la interfaz web ---

@main_bp.route('/')
def index():
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_value = db.session.query(func.sum(Product.price * Product.stock)).scalar() or 0
    
    low_stock_products = Product.query.filter(Product.stock < 10).limit(5).all()
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    
    return render_template('index.html',
        total_products=total_products,
        total_categories=total_categories,
        total_value=total_value,
        low_stock_products=low_stock_products,
        recent_products=recent_products
    )

@main_bp.route('/products')
def products():
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    
    query = Product.query
    
    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) |
            (Product.sku.ilike(f'%{search}%'))
        )
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.order_by(Product.created_at.desc()).all()
    categories = Category.query.all()
    
    return render_template('products.html',
        products=products,
        categories=categories
    )

@main_bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)
