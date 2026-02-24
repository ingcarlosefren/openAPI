# 🚀 Users & Articles Management API

API REST para la gestión de usuarios (roles y perfiles) y artículos (categorías y valoraciones), construida con **Python**, **FastAPI** y siguiendo los principios de **Arquitectura Hexagonal** y **DDD**.

---

## 🛠️ Stack Tecnológico

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Base de Datos:** SQLite3 (vía SQLAlchemy 2.0 Async)
* **Validación:** Pydantic v2
* **Testing:** Pytest
* **Documentación:** OpenAPI 3.0 (Swagger)

---

## 🏗️ Arquitectura del Proyecto

Este proyecto utiliza **Arquitectura Hexagonal (Ports & Adapters)** para garantizar el desacoplamiento entre la lógica de negocio y las dependencias técnicas.

* **Dominio:** Reglas de negocio puras (Entidades, Value Objects).
* **Aplicación:** Casos de uso del sistema.
* **Infraestructura:** Adaptadores para base de datos y servicios externos.
* **API/App:** Adaptadores de entrada (Endpoints).

> Para más detalles, consulta el archivo [arquitectura.md](./arquitectura.md).

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone [https://github.com/ingcarlosefren/openAPI.git](https://github.com/ingcarlosefren/openAPI.git)
cd openAPI/api-test
```
### 2. Configurar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Ejecutar la API
```bash
uvicorn src.app.main:app --reload
```
La API estará disponible en http://localhost:8080/v1.

### 📖 Documentación
Una vez ejecutada la API, puedes acceder a la documentación interactiva:

Swagger UI: http://localhost:8080/docs

ReDoc: http://localhost:8080/redoc

Especificación: El contrato original se encuentra en openapi.yaml.

Health check: http://localhost:8080/v1/health

### 🧪 Testing
Para ejecutar la suite de pruebas (Unitarias, Integración y E2E):
```bash
# Ejecutar todos los tests
pytest -v

# Ejecutar con reporte de cobertura
pytest --cov=src
```

### 🤖 Guía para Agentes de IA
Si estás utilizando un agente de IA para desarrollar este proyecto:

1. Lee el archivo .agent/instructions.md para conocer las reglas de codificación.

2. Consulta .agent/context.md para entender el progreso actual.

3. Respeta estrictamente el contrato definido en openapi.yaml.