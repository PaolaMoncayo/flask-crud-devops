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

```bash
cp .env.example .env
# Edita el archivo .env con tus configuraciones personales
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
git checkout -b develop
git push origin develop

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

## 5. Comunicación y Colaboración

- **GitHub Discussions** para temas técnicos.
- **WhatsApp/Telegram** para comunicación rápida.
- **Google Docs** para documentación compartida.
- **Reuniones semanales** para sincronización.

---

## 6. Reflexión Intercultural

### Resolución de Conflictos

- Usamos herramientas visuales de merge (VSCode, GitHub).
- Antes de resolver un conflicto, nos comunicamos por WhatsApp o GitHub Discussions para entender el contexto.
- Documentamos las decisiones importantes en los PRs y en Google Docs.

### Herramientas de Comunicación

- GitHub Discussions para temas técnicos y dudas.
- WhatsApp/Telegram para avisos urgentes o coordinación rápida.
- Google Docs para actas de reuniones y documentación de decisiones.

### Consideraciones de Husos Horarios

- Documentamos los horarios de trabajo de cada miembro en Google Docs.
- Usamos herramientas asíncronas (GitHub, Google Docs) para que todos puedan avanzar a su ritmo.
- Establecemos ventanas de tiempo para reuniones donde todos puedan coincidir.

### Análisis de desafíos interculturales y técnicos

> Trabajar en un equipo distribuido internacionalmente nos obligó a ser muy claros en la comunicación y a documentar todo. Los conflictos de merge se resolvieron con diálogo y herramientas visuales, priorizando siempre la comprensión mutua. La diferencia de husos horarios nos llevó a planificar tareas asíncronas y a respetar los tiempos de respuesta de cada miembro. El uso de GitHub Actions y Slack permitió que todos estuviéramos informados sobre el estado del proyecto, sin importar la hora o el lugar. La colaboración intercultural enriqueció el proyecto, aportando diferentes perspectivas y soluciones creativas a los problemas técnicos y organizativos.

---

## 7. Contribuidores

- Paola Moncayo [Colombia]
- [Agrega aquí los nombres y países de los demás miembros]

---

## 8. Licencia

MIT

---

## 9. Recursos útiles

- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Documentación de GitHub Actions](https://docs.github.com/en/actions)
- [Guía de buenas prácticas de Git](https://www.atlassian.com/git/tutorials/comparing-workflows)

---
