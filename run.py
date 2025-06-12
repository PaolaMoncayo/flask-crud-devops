from http.server import HTTPServer
from server import RequestHandler
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def run_server():
    # Obtener el puerto del archivo .env o usar 8000 por defecto
    port = int(os.getenv('PORT', 8000))
    
    # Configurar el servidor
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    
    print(f"Servidor iniciado en http://localhost:{port}")
    print("Presiona Ctrl+C para detener el servidor")
    
    try:
        # Iniciar el servidor
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        httpd.server_close()

if __name__ == '__main__':
    run_server() 