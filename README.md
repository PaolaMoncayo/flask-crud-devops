# Proyecto CRUD - Colaboración Internacional

## Estructura del Proyecto
Este proyecto implementa un sistema CRUD (Create, Read, Update, Delete) utilizando Flask y MySQL, con un enfoque en colaboración internacional y desarrollo distribuido.

### Ramas del Proyecto
- `main`: Rama principal, solo integraciones validadas
- `develop`: Rama para nuevas funcionalidades
- `test`: Rama para pruebas y validación

## Configuración del Entorno
1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

## Estructura de Commits
Seguimos el formato:
```
tipo: descripción [País]

Ejemplos:
- feat: Added login feature [México]
- fix: Fixed database connection [España]
- test: Added user authentication tests [Colombia]
```

## Proceso de Desarrollo
1. Crear una rama desde `develop` para tu feature
2. Desarrollar y probar localmente
3. Hacer commit con mensaje descriptivo
4. Crear Pull Request a `develop`
5. Esperar revisión y aprobación
6. Merge a `develop` después de aprobación

## Integración Continua
- GitHub Actions ejecuta tests automáticamente
- Notificaciones en Discord/Slack para builds fallidos

## Comunicación y Colaboración
- GitHub Discussions para discusiones técnicas
- WhatsApp/Telegram para comunicación rápida
- Reuniones semanales para sincronización

## Reflexión Intercultural
### Resolución de Conflictos
- Uso de herramientas de merge visuales
- Comunicación clara antes de resolver conflictos
- Documentación de decisiones importantes

### Herramientas de Comunicación
- GitHub Discussions para temas técnicos
- WhatsApp/Telegram para comunicación inmediata
- Documentación compartida en Google Docs

### Consideraciones de Husos Horarios
- Documentación clara de horarios de trabajo
- Uso de herramientas asíncronas
- Establecimiento de ventanas de tiempo para reuniones

## Contribuidores
- [Lista de contribuidores por país]

## Licencia
[Especificar licencia] 