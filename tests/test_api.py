import pytest
import json
from http.server import HTTPServer
from server import RequestHandler
import threading
import requests
import time

@pytest.fixture(scope="function")
def server():
    """Fixture que proporciona un servidor HTTP para pruebas"""
    # Iniciar el servidor en un hilo separado
    server = HTTPServer(('localhost', 8000), RequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    # Dar tiempo para que el servidor inicie
    time.sleep(1)
    
    yield server
    
    # Limpiar
    server.shutdown()
    server.server_close()

def test_get_categories(server):
    """Prueba obtener todas las categorías"""
    # Crear una categoría primero
    response = requests.post(
        'http://localhost:8000/api/categories',
        json={'name': 'Electrónicos', 'description': 'Productos electrónicos'}
    )
    assert response.status_code == 201
    
    # Obtener categorías
    response = requests.get('http://localhost:8000/api/categories')
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 1
    assert categories[0]['name'] == 'Electrónicos'

def test_create_category(server):
    """Prueba crear una categoría"""
    response = requests.post(
        'http://localhost:8000/api/categories',
        json={'name': 'Ropa', 'description': 'Ropa y accesorios'}
    )
    assert response.status_code == 201
    data = response.json()
    assert data['message'] == 'Categoría creada'

def test_delete_category(server):
    """Prueba eliminar una categoría"""
    # Crear una categoría primero
    response = requests.post(
        'http://localhost:8000/api/categories',
        json={'name': 'Test Delete', 'description': 'Para eliminar'}
    )
    assert response.status_code == 201
    
    # Obtener el ID de la categoría
    response = requests.get('http://localhost:8000/api/categories')
    categories = response.json()
    category_id = categories[0]['id']
    
    # Eliminar la categoría
    response = requests.delete(f'http://localhost:8000/api/categories/{category_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Categoría eliminada'

def test_get_products(server):
    """Prueba obtener todos los productos"""
    # Crear una categoría primero
    response = requests.post(
        'http://localhost:8000/api/categories',
        json={'name': 'Electrónicos', 'description': 'Productos electrónicos'}
    )
    assert response.status_code == 201
    
    # Obtener el ID de la categoría
    response = requests.get('http://localhost:8000/api/categories')
    categories = response.json()
    category_id = categories[0]['id']
    
    # Crear un producto
    response = requests.post(
        'http://localhost:8000/api/products',
        json={
            'name': 'Laptop',
            'description': 'Laptop HP',
            'price': 999.99,
            'stock': 10,
            'category_id': category_id
        }
    )
    assert response.status_code == 201
    
    # Obtener productos
    response = requests.get('http://localhost:8000/api/products')
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 1
    assert products[0]['name'] == 'Laptop'

def test_create_product(server):
    """Prueba crear un producto"""
    # Crear una categoría primero
    response = requests.post(
        'http://localhost:8000/api/categories',
        json={'name': 'Electrónicos', 'description': 'Productos electrónicos'}
    )
    assert response.status_code == 201
    
    # Obtener el ID de la categoría
    response = requests.get('http://localhost:8000/api/categories')
    categories = response.json()
    category_id = categories[0]['id']
    
    # Crear un producto
    response = requests.post(
        'http://localhost:8000/api/products',
        json={
            'name': 'Mouse',
            'description': 'Mouse inalámbrico',
            'price': 29.99,
            'stock': 20,
            'category_id': category_id
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data['message'] == 'Producto creado'

def test_delete_product(server):
    """Prueba eliminar un producto"""
    # Crear una categoría primero
    response = requests.post(
        'http://localhost:8000/api/categories',
        json={'name': 'Electrónicos', 'description': 'Productos electrónicos'}
    )
    assert response.status_code == 201
    
    # Obtener el ID de la categoría
    response = requests.get('http://localhost:8000/api/categories')
    categories = response.json()
    category_id = categories[0]['id']
    
    # Crear un producto
    response = requests.post(
        'http://localhost:8000/api/products',
        json={
            'name': 'Test Delete',
            'description': 'Para eliminar',
            'price': 99.99,
            'stock': 5,
            'category_id': category_id
        }
    )
    assert response.status_code == 201
    
    # Obtener el ID del producto
    response = requests.get('http://localhost:8000/api/products')
    products = response.json()
    product_id = products[0]['id']
    
    # Eliminar el producto
    response = requests.delete(f'http://localhost:8000/api/products/{product_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Producto eliminado' 