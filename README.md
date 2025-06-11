# Proyecto CRUD - Colaboración Internacional

Este proyecto implementa un sistema CRUD (Create, Read, Update, Delete) utilizando Flask y MySQL, con un enfoque en colaboración internacional y desarrollo distribuido.

---

## 1. Estructura del Proyecto

- `main`: Rama principal, solo integraciones validadas.
- `develop`: Rama para nuevas funcionalidades.
- `test`: Rama para pruebas y validación.

---

## 2. Configuración del Entorno

### Clonar el repositorio

```bash
git clone https://github.com/PaolaMoncayo/flask-crud-devops.git
cd flask-crud-devops
```

### Crear y activar entorno virtual

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto basado en el siguiente ejemplo:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario
DB_PASSWORD=contraseña
DB_NAME=nombre_base_datos

FLASK_ENV=development
SECRET_KEY=tu_clave_secreta
```

---

## 3. Flujo de Trabajo con Git y GitHub

### 1. Configurar usuario de Git

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tuemail@ejemplo.com"
```

### 2. Crear ramas principales

```bash
git checkout main
git pull origin main
git checkout -b develop
git push origin develop
git checkout main
git checkout -b test
git push origin test
```

### 3. Crear una rama para tu feature (desde develop)

```bash
git checkout develop
git pull origin develop
git checkout -b feat/login
```

### 4. Hacer cambios y commit

```bash
git add .
git commit -m "feat: Added login feature [México]"
```

### 5. Sincronizar cambios antes de subir

```bash
git pull origin develop
```

### 6. Subir tu rama al repositorio

```bash
git push origin feat/login
```

### 7. Crear Pull Request (PR)

- Ve a GitHub y crea un PR de tu rama hacia `develop`.
- Etiqueta a tus compañeros para revisión (simulando husos horarios).

### 8. Revisar y resolver conflictos

- Si hay conflictos, comunícate con tu equipo y resuélvelos usando herramientas visuales de merge (VSCode, GitHub, etc).
- Documenta las decisiones importantes en el PR.

---

## 4. Integración DevOps

### GitHub Actions

- Al hacer push o PR a `main`, `develop` o `test`, se ejecutan los tests automáticamente.
- Si un build falla, se envía una notificación a Slack.

#### Ejemplo de archivo `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop, test ]
  pull_request:
    branches: [ main, develop, test ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.13'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      env:
        FLASK_APP: app.py
        FLASK_ENV: testing
        DATABASE_URL: mysql://root:root@localhost:3306/test_db
      run: |
        pytest tests/ --cov=app --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
    - name: Notify on failure
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        fields: repo,message,commit,author,action,eventName,ref,workflow,job,took
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
      continue-on-error: true
```

---

## 5. Ejecución y Evidencias

### App Flask corriendo

![App Flask en ejecución](docs/img/flask-app-running.png)

### Notificación de Slack funcionando

![Notificación Slack](docs/img/slack-notification.png)

### Commits en ramas de pruebas

- **Rama develop:**
  ![Commits en develop](docs/img/commits-develop.png)
- **Rama test:**
  ![Commits en test](docs/img/commits-test.png)

### Ejecución de tests

![Tests ejecutándose](docs/img/tests-running.png)

---

## 6. Comunicación y Colaboración

- **WhatsApp/Telegram** para comunicación rápida.
- **Google Docs** para documentación compartida.

---

## 7. Reflexión Intercultural

### Resolución de Conflictos

- Usamos herramientas visuales de merge (VSCode, GitHub).
- Antes de resolver un conflicto, nos comunicamos por WhatsApp para entender el contexto.
- Documentamos las decisiones importantes en Google Docs.

### Herramientas de Comunicación

- WhatsApp/Telegram para avisos urgentes o coordinación rápida.
- Google Docs para actas de reuniones y documentación de decisiones.

### Consideraciones de Husos Horarios

- Documentamos los horarios de trabajo de cada miembro en Google Docs.
- Usamos herramientas asíncronas (GitHub, Google Docs) para que todos puedan avanzar a su ritmo.
- Establecemos ventanas de tiempo para reuniones donde todos puedan coincidir.

### Análisis de desafíos interculturales y técnicos

> Trabajar en un equipo distribuido internacionalmente nos obligó a ser muy claros en la comunicación y a documentar todo. Los conflictos de merge se resolvieron con diálogo y herramientas visuales, priorizando siempre la comprensión mutua. La diferencia de husos horarios nos llevó a planificar tareas asíncronas y a respetar los tiempos de respuesta de cada miembro. El uso de GitHub Actions y Slack permitió que todos estuviéramos informados sobre el estado del proyecto, sin importar la hora o el lugar. La colaboración intercultural enriqueció el proyecto, aportando diferentes perspectivas y soluciones creativas a los problemas técnicos y organizativos.

---

## 8. Contribuidores

- Paola Moncayo [Colombia]
- [Agrega aquí los nombres y países de los demás miembros]

---

## 9. Licencia

MIT

---

## 10. Recursos útiles

- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Documentación de GitHub Actions](https://docs.github.com/en/actions)
- [Guía de buenas prácticas de Git](https://www.atlassian.com/git/tutorials/comparing-workflows)

---

## 11. Estructura de carpetas para imágenes

```
flask-crud-devops/
│
├── docs/
│   └── img/
│       ├── flask-app-running.png
│       ├── slack-notification.png
│       ├── commits-develop.png
│       ├── commits-test.png
│       └── tests-running.png
```

---
