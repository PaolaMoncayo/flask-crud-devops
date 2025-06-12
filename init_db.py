import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def init_database():
    try:
        # Primero conectamos sin especificar la base de datos
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'password')
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear la base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'crud_db')}")
            cursor.execute(f"USE {os.getenv('DB_NAME', 'crud_db')}")
            
            # Crear tabla de categorías
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                )
            """)
            
            # Crear tabla de productos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    stock INT NOT NULL,
                    category_id INT,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)
            
            connection.commit()
            print("Base de datos inicializada correctamente")
            
    except Error as e:
        print(f"Error inicializando la base de datos: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    init_database() 