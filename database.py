import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Database:
    def __init__(self):
        # Asegurarnos de que las variables de entorno estén cargadas
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'database': os.getenv('DB_NAME', 'crud_db')
        }
        
        # Imprimir la configuración (sin la contraseña) para debug
        debug_config = self.config.copy()
        debug_config['password'] = '****'
        print("Configuración de la base de datos:", debug_config)
        
        self.init_db()

    def get_connection(self):
        try:
            # Intentar conexión con la base de datos
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                print("Conexión exitosa a MySQL")
                return connection
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            # Intentar conexión sin base de datos
            try:
                connection = mysql.connector.connect(
                    host=self.config['host'],
                    user=self.config['user'],
                    password=self.config['password']
                )
                if connection.is_connected():
                    print("Conexión exitosa a MySQL (sin base de datos)")
                    return connection
            except Error as e:
                print(f"Error en segundo intento de conexión: {e}")
        return None

    def init_db(self):
        try:
            # Primero crear la base de datos si no existe
            connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password']
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                
                # Crear base de datos
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
                cursor.execute(f"USE {self.config['database']}")
                
                # Crear tabla de categorías
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Crear tabla de productos
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    stock INT NOT NULL,
                    category_id INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                    ON DELETE SET NULL
                )
                ''')
                
                connection.commit()
                print("Base de datos inicializada correctamente")
            
        except Error as e:
            print(f"Error inicializando la base de datos: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("Conexión a MySQL cerrada")

    # Métodos para Categorías
    def get_all_categories(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM categories ORDER BY name')
            categories = cursor.fetchall()
            conn.close()
            return categories
        except Error as e:
            print(f"Error obteniendo categorías: {e}")
            return []

    def create_category(self, name, description):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO categories (name, description) VALUES (%s, %s)',
                         (name, description))
            conn.commit()
            category_id = cursor.lastrowid
            conn.close()
            return {'id': category_id, 'name': name, 'description': description}
        except Error as e:
            print(f"Error creando categoría: {e}")
            return None

    def update_category(self, category_id, name, description):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE categories SET name = %s, description = %s WHERE id = %s',
                         (name, description, category_id))
            conn.commit()
            conn.close()
            return {'id': category_id, 'name': name, 'description': description}
        except Error as e:
            print(f"Error actualizando categoría: {e}")
            return None

    def delete_category(self, category_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM categories WHERE id = %s', (category_id,))
            conn.commit()
            conn.close()
            return True
        except Error as e:
            print(f"Error eliminando categoría: {e}")
            return False

    # Métodos para Productos
    def get_all_products(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.*, c.name as category_name 
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.id
                ORDER BY p.name
            ''')
            products = cursor.fetchall()
            
            # Convertir valores decimales a float
            for product in products:
                if 'price' in product and product['price'] is not None:
                    product['price'] = float(product['price'])
            
            conn.close()
            return products
        except Error as e:
            print(f"Error obteniendo productos: {e}")
            return []

    def create_product(self, name, description, price, stock, category_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Asegurarnos de que price sea float
            price = float(price)
            
            cursor.execute('''
                INSERT INTO products (name, description, price, stock, category_id) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, description, price, stock, category_id))
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            return {
                'id': product_id,
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
                'category_id': category_id
            }
        except Error as e:
            print(f"Error creando producto: {e}")
            return None

    def update_product(self, product_id, name, description, price, stock, category_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Asegurarnos de que price sea float
            price = float(price)
            
            cursor.execute('''
                UPDATE products 
                SET name = %s, description = %s, price = %s, stock = %s, category_id = %s 
                WHERE id = %s
            ''', (name, description, price, stock, category_id, product_id))
            conn.commit()
            conn.close()
            return {
                'id': product_id,
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
                'category_id': category_id
            }
        except Error as e:
            print(f"Error actualizando producto: {e}")
            return None

    def delete_product(self, product_id):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
            conn.commit()
            conn.close()
            return True
        except Error as e:
            print(f"Error eliminando producto: {e}")
            return False

    def clean_tables(self):
        """Limpia todas las tablas de la base de datos"""
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products")
                cursor.execute("DELETE FROM categories")
                conn.commit()
            except Error as e:
                print(f"Error al limpiar las tablas: {e}")
            finally:
                cursor.close()
                conn.close() 