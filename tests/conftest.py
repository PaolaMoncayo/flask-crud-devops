import pytest
from app import create_app, db
from app.models import Category, Product
from app.config import TestingConfig

@pytest.fixture
def app():
    """Crear y configurar una nueva instancia de la aplicación para cada prueba"""
    app = create_app(TestingConfig)
    
    # Crear el contexto de la aplicación
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        yield app
        
        # Limpiar después de cada prueba
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """Cliente con autenticación simulada si es necesario"""
    return client

@pytest.fixture
def sample_category(app):
    """Categoría de muestra para pruebas"""
    with app.app_context():
        # Crear dos categorías de prueba
        category1 = Category(
            name="Categoría de Prueba 1",
            description="Descripción de prueba 1"
        )
        category2 = Category(
            name="Categoría de Prueba 2",
            description="Descripción de prueba 2"
        )
        db.session.add_all([category1, category2])
        db.session.commit()
        
        # Refrescar la sesión para asegurar que las instancias estén vinculadas
        db.session.refresh(category1)
        return category1

@pytest.fixture
def sample_product(app, sample_category):
    """Producto de muestra para pruebas"""
    with app.app_context():
        product = Product(
            sku="TEST-001",
            name="Test Product",
            description="Test Description",
            price=99.99,
            stock=10,
            category_id=sample_category.id
        )
        db.session.add(product)
        db.session.commit()
        
        # Refrescar la sesión para asegurar que la instancia esté vinculada
        db.session.refresh(product)
        return product
