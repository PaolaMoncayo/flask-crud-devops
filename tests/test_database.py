import pytest
from database import Database
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

@pytest.fixture
def db():
    # Configurar una base de datos de prueba
    test_db = Database()
    # Limpiar las tablas antes de cada prueba
    conn = test_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM categories")
    conn.commit()
    cursor.close()
    conn.close()
    return test_db

def test_create_category(test_db):
    """Prueba la creación de una categoría"""
    category = test_db.create_category("Electrónicos", "Productos electrónicos")
    assert category is not None
    assert category['name'] == "Electrónicos"
    assert category['description'] == "Productos electrónicos"

def test_get_all_categories(test_db):
    """Prueba obtener todas las categorías"""
    # Crear algunas categorías
    test_db.create_category("Electrónicos", "Productos electrónicos")
    test_db.create_category("Ropa", "Ropa y accesorios")

    # Obtener todas las categorías
    categories = test_db.get_all_categories()
    assert len(categories) == 2
    assert categories[0]['name'] == "Electrónicos"
    assert categories[1]['name'] == "Ropa"

def test_create_product(test_db):
    """Prueba la creación de un producto"""
    # Crear una categoría primero
    category = test_db.create_category("Electrónicos", "Productos electrónicos")
    
    # Crear un producto
    product = test_db.create_product(
        "Laptop",
        "Laptop HP",
        999.99,
        10,
        category['id']
    )
    assert product is not None
    assert product['name'] == "Laptop"
    assert product['price'] == 999.99
    assert product['stock'] == 10
    assert product['category_id'] == category['id']

def test_get_all_products(test_db):
    """Prueba obtener todos los productos"""
    # Crear una categoría
    category = test_db.create_category("Electrónicos", "Productos electrónicos")

    # Crear algunos productos
    test_db.create_product("Laptop", "Laptop HP", 999.99, 10, category['id'])
    test_db.create_product("Mouse", "Mouse inalámbrico", 29.99, 20, category['id'])

    # Obtener todos los productos
    products = test_db.get_all_products()
    assert len(products) == 2
    assert products[0]['name'] == "Laptop"
    assert products[1]['name'] == "Mouse"

def test_delete_category(test_db):
    """Prueba eliminar una categoría"""
    # Crear una categoría
    category = test_db.create_category("Electrónicos", "Productos electrónicos")

    # Eliminar la categoría
    result = test_db.delete_category(category['id'])
    assert result is True

    # Verificar que se eliminó
    categories = test_db.get_all_categories()
    assert len(categories) == 0

def test_delete_product(test_db):
    """Prueba eliminar un producto"""
    # Crear una categoría y un producto
    category = test_db.create_category("Electrónicos", "Productos electrónicos")
    product = test_db.create_product("Laptop", "Laptop HP", 999.99, 10, category['id'])

    # Eliminar el producto
    result = test_db.delete_product(product['id'])
    assert result is True

    # Verificar que se eliminó
    products = test_db.get_all_products()
    assert len(products) == 0

def test_update_category(test_db):
    """Prueba actualizar una categoría"""
    # Crear una categoría
    category = test_db.create_category("Electrónicos", "Productos electrónicos")

    # Actualizar la categoría
    updated = test_db.update_category(category['id'], "Electrónicos Nuevos", "Nueva descripción")
    assert updated is True

    # Verificar la actualización
    categories = test_db.get_all_categories()
    assert len(categories) == 1
    assert categories[0]['name'] == "Electrónicos Nuevos"
    assert categories[0]['description'] == "Nueva descripción"

def test_update_product(test_db):
    """Prueba actualizar un producto"""
    # Crear una categoría y un producto
    category = test_db.create_category("Electrónicos", "Productos electrónicos")
    product = test_db.create_product("Laptop", "Laptop HP", 999.99, 10, category['id'])

    # Actualizar el producto
    updated = test_db.update_product(
        product['id'],
        "Laptop Pro",
        "Laptop HP Pro",
        1299.99,
        5,
        category['id']
    )
    assert updated is True

    # Verificar la actualización
    products = test_db.get_all_products()
    assert len(products) == 1
    assert products[0]['name'] == "Laptop Pro"
    assert products[0]['price'] == 1299.99
    assert products[0]['stock'] == 5

def test_product_without_category(test_db):
    """Prueba crear un producto sin categoría"""
    # Crear un producto sin categoría
    product = test_db.create_product(
        "Laptop",
        "Laptop HP",
        999.99,
        10,
        None
    )
    assert product is not None
    assert product['category_id'] is None

    # Verificar que se puede obtener
    products = test_db.get_all_products()
    assert len(products) == 1
    assert products[0]['category_id'] is None 