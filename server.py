from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from database import Database
import os

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = Database()
        super().__init__(*args, **kwargs)

    def _set_headers(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _send_json_response(self, data):
        self._set_headers('application/json')
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        # Servir el archivo index.html
        if self.path == '/':
            self.serve_file('templates/index.html')
        # API endpoints
        elif self.path == '/api/categories':
            self.get_categories()
        elif self.path == '/api/products':
            self.get_products()
        else:
            self.send_error(404, "Ruta no encontrada")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == '/api/categories':
            self.create_category(data)
        elif self.path == '/api/products':
            self.create_product(data)
        else:
            self.send_error(404, "Ruta no encontrada")

    def do_DELETE(self):
        """Maneja las peticiones DELETE"""
        if self.path.startswith('/api/categories/'):
            try:
                category_id = int(self.path.split('/')[-1])
                if self.db.delete_category(category_id):
                    self._send_json_response({'message': 'Categoría eliminada'})
                else:
                    self.send_error(404, 'Categoría no encontrada')
            except ValueError:
                self.send_error(400, 'ID de categoría inválido')
        elif self.path.startswith('/api/products/'):
            try:
                product_id = int(self.path.split('/')[-1])
                if self.db.delete_product(product_id):
                    self._send_json_response({'message': 'Producto eliminado'})
                else:
                    self.send_error(404, 'Producto no encontrado')
            except ValueError:
                self.send_error(400, 'ID de producto inválido')
        else:
            self.send_error(404, 'Ruta no encontrada')

    def serve_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "Archivo no encontrado")

    def get_categories(self):
        try:
            categories = self.db.get_all_categories()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(categories).encode())
        except Exception as e:
            self.send_error(500, str(e))

    def get_products(self):
        try:
            products = self.db.get_all_products()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(products).encode())
        except Exception as e:
            self.send_error(500, str(e))

    def create_category(self, data):
        try:
            self.db.create_category(data['name'], data['description'])
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Categoría creada"}).encode())
        except Exception as e:
            self.send_error(500, str(e))

    def create_product(self, data):
        try:
            self.db.create_product(
                data['name'],
                data['description'],
                float(data['price']),
                int(data['stock']),
                int(data['category_id']) if data.get('category_id') else None
            )
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Producto creado"}).encode())
        except Exception as e:
            self.send_error(500, str(e))

    def delete_category(self, category_id):
        try:
            self.db.delete_category(category_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Categoría eliminada"}).encode())
        except Exception as e:
            self.send_error(500, str(e))

    def delete_product(self, product_id):
        try:
            self.db.delete_product(product_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Producto eliminado"}).encode())
        except Exception as e:
            self.send_error(500, str(e))

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Servidor iniciado en el puerto {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 