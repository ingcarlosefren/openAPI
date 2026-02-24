# Agent Rules & Coding Standards

Eres un experto en Python, FastAPI y Arquitectura Hexagonal. Tu objetivo es implementar la API siguiendo estas reglas estrictas:

### Principios de Implementación
1. **Domain First**: Antes de escribir un Endpoint o un Repositorio, debes definir la Entidad de Dominio en `modules/{module}/domain/models/`.
2. **No Shortcuts**: No permitas que la capa de Infraestructura (SQLAlchemy) contamine el Dominio. Usa siempre Mappers.
3. **Typing**: Usa Type Hints de Python 3.11+ en todas las funciones.
4. **Async**: Todo el código de entrada (FastAPI) y salida (DB) debe ser `async`.

### Especificaciones Técnicas
- **Database**: Usa SQLAlchemy 2.0 con el driver `aiosqlite`.
- **Schemas**: Usa Pydantic v2 para validar los requests según el `openapi.yaml`.
- **Naming**: 
    - Casos de uso: `create_user_use_case.py`
    - Puertos: `user_repository.py` (Clase abstracta)
    - Adaptadores: `sqlalchemy_user_repository.py`

### Reglas para el Agente sobre Tests
- **Test-Driven Development (TDD):** El agente debe ser capaz de proponer los tests antes de la implementación si se solicita.
- **Aislamiento:** Los tests unitarios de los casos de uso NO deben importar `SQLAlchemy` ni `FastAPI`. Deben usar el Puerto (Interfaz) mockeado.
- **Cobertura:** Se espera una cobertura mínima del 80%, priorizando la capa de `Domain` y `Application`.
- **Comando de ejecución:** `pytest -v`.    