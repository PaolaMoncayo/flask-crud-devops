import pytest
import os
from dotenv import load_dotenv
from database import Database

# Cargar variables de entorno
load_dotenv()

@pytest.fixture(scope="function")
def test_db():
    # Crear una instancia de la base de datos
    db = Database()
    
    # Limpiar las tablas antes de cada prueba
    db.clean_tables()
    
    yield db
    
    # Limpiar las tablas después de cada prueba
    db.clean_tables() 