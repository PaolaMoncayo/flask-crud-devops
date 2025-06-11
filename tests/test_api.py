import json
import pytest
from app.models import Category, Product

# Pruebas de Categorías
def test_list_categories(client, sample_category):
    """Prueba obtener lista de categorías"""
    res = client.get("/api/categories")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Deberían existir al menos las categorías de prueba

def test_create_category(client):
    """Prueba crear una nueva categoría"""
    res = client.post("/api/categories", json={
        "name": "TestCat",
        "description": "Descripción de prueba"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "TestCat"
    assert data["description"] == "Descripción de prueba"
    assert "id" in data

def test_get_category(client, sample_category):
    """Prueba obtener una categoría específica"""
    res = client.get(f"/api/categories/{sample_category.id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["name"] == sample_category.name
    assert data["description"] == sample_category.description

def test_update_category(client):
    """Prueba actualizar una categoría"""
    # Crear primero
    res = client.post("/api/categories", json={"name": "CatUp", "description": "desc"})
    cat_id = res.get_json()["id"]
    # Actualizar
    res = client.put(f"/api/categories/{cat_id}", json={"name": "CatUpdated", "description": "Nueva desc"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["name"] == "CatUpdated"
    assert data["description"] == "Nueva desc"

def test_delete_category(client):
    """Prueba eliminar una categoría"""
    res = client.post("/api/categories", json={"name": "CatDel", "description": "desc"})
    cat_id = res.get_json()["id"]
    res = client.delete(f"/api/categories/{cat_id}")
    assert res.status_code == 204
    # Ya no debe existir
    res = client.get(f"/api/categories/{cat_id}")
    assert res.status_code == 404

# Pruebas de Productos
def test_list_products(client):
    """Prueba obtener lista de productos"""
    res = client.get("/api/products")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)

def test_create_product(client):
    """Prueba crear un nuevo producto"""
    # Crear categoría primero
    res = client.post("/api/categories", json={"name": "CatProd", "description": "desc"})
    cat_id = res.get_json()["id"]
    # Crear producto
    prod_data = {
        "sku": "SKU001",
        "name": "Producto Test",
        "description": "Desc prod",
        "price": 10.5,
        "stock": 5,
        "category_id": cat_id
    }
    res = client.post("/api/products", json=prod_data)
    assert res.status_code == 201
    data = res.get_json()
    assert data["sku"] == "SKU001"
    assert data["name"] == "Producto Test"
    assert data["stock"] == 5
    assert data["category"]["id"] == cat_id

def test_get_product(client, sample_product):
    """Prueba obtener un producto específico"""
    res = client.get(f"/api/products/{sample_product.id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["sku"] == sample_product.sku
    assert data["name"] == sample_product.name
    assert float(data["price"]) == float(sample_product.price)

def test_update_product(client):
    """Prueba actualizar un producto"""
    # Crear categoría y producto
    res = client.post("/api/categories", json={"name": "CatUpProd", "description": "desc"})
    cat_id = res.get_json()["id"]
    prod_data = {
        "sku": "SKU002",
        "name": "ProdUp",
        "description": "Desc",
        "price": 20.0,
        "stock": 2,
        "category_id": cat_id
    }
    res = client.post("/api/products", json=prod_data)
    prod_id = res.get_json()["id"]
    # Actualizar
    res = client.put(f"/api/products/{prod_id}", json={
        "sku": "SKU002",
        "name": "ProdUpdated",
        "description": "Nueva desc",
        "price": 25.0,
        "stock": 10,
        "category_id": cat_id
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["name"] == "ProdUpdated"
    assert data["stock"] == 10

def test_delete_product(client):
    """Prueba eliminar un producto"""
    res = client.post("/api/categories", json={"name": "CatDelProd", "description": "desc"})
    cat_id = res.get_json()["id"]
    prod_data = {
        "sku": "SKU003",
        "name": "ProdDel",
        "description": "Desc",
        "price": 30.0,
        "stock": 1,
        "category_id": cat_id
    }
    res = client.post("/api/products", json=prod_data)
    prod_id = res.get_json()["id"]
    res = client.delete(f"/api/products/{prod_id}")
    assert res.status_code == 204
    # Ya no debe existir
    res = client.get(f"/api/products/{prod_id}")
    assert res.status_code == 404

# Pruebas de validación
def test_create_product_invalid_data(client, sample_category):
    """Prueba crear producto con datos inválidos"""
    # Falta el campo sku
    res = client.post("/api/products", json={
        "name": "Producto Inválido",
        "price": 99.99,
        "stock": 10,
        "category_id": sample_category.id
    })
    assert res.status_code == 400

def test_create_category_invalid_data(client):
    """Prueba crear categoría con datos inválidos"""
    # Falta el campo name
    res = client.post("/api/categories", json={
        "description": "Descripción sin nombre"
    })
    assert res.status_code == 400

# Pruebas de relaciones
def test_category_product_relationship(client, sample_category, sample_product):
    """Prueba la relación entre categoría y productos"""
    res = client.get(f"/api/categories/{sample_category.id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["product_count"] == 1  # Debería tener un producto
