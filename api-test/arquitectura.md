# Especificación Técnica: Arquitectura Hexagonal + DDD

Este documento define la arquitectura para la implementación de la API **Users & Articles Management**, basada en el estándar OpenAPI 3.0.3 proporcionado.

---

## Stack Tecnológico
* **Lenguaje:** Python 3.11+
* **Framework:** FastAPI
* **Validación:** Pydantic v2
* **ORM:** SQLAlchemy 2.0 (Asyncio)
* **Base de Datos:** SQLite3 (database.db)

---

## Estructura de Proyecto

```text
src/
├── app/                        # Capa de Entrada (Adaptadores Primarios)
│   ├── main.py                 # Configuración de FastAPI y Middleware
│   ├── api/                    # Routers (Controllers)
│   │   ├── v1/                 # Versionamiento
│   │   │   ├── users.py        # Endpoints de /users
│   │   │   ├── articles.py     # Endpoints de /articles
│   │   │   └── health.py       # Endpoints de /health
│   │   └── dependencies.py     # Inyección de dependencias
│
├── modules/                    # Lógica de Negocio (Bounded Contexts)
│   ├── users/                  
│   │   ├── domain/             # Corazón del negocio
│   │   │   ├── models/         # Entidades (User) y Value Objects
│   │   │   ├── repository.py   # Puerto (Interfaz del repositorio)
│   │   │   └── exceptions.py   # Excepciones de dominio
│   │   ├── application/        # Casos de Uso (Orquestación)
│   │   │   ├── create_user.py
│   │   │   ├── get_user.py
│   │   │   └── update_user.py
│   │   └── infrastructure/     # Adaptadores Secundarios
│   │       ├── persistence/    # Repositorio SQLAlchemy
│   │       └── mappers/        # Transformadores de datos
│   │
│   ├── articles/               # Módulo de Artículos (Misma estructura)
│   │
│   └── shared/                 # Kernel compartido
│       ├── domain/             # Tipos base (UUID, Email, etc.)
│       └── infrastructure/     # Configuración de DB y Logs
│
└── database.db                 # SQLite local

Capas y Responsabilidades
1. Dominio (/domain)
Es el núcleo del sistema. Contiene:

Entidades: User (id, name, email, role, birthDate) y Article (id, title, content, author, category).

Value Objects: Lógica para validar el Email y los Enums de Roles y Categorías.

Puertos: Interfaces abstractas como IUserRepository.

2. Aplicación (/application)
Implementa los casos de uso descritos en los operationId del OpenAPI:

createUser, getUsers, patchUser.

createArticle, getArticles, getArticlesByUser.

3. Infraestructura (/infrastructure)
Implementación de persistencia con SQLAlchemy.

Transformación de modelos de DB a Entidades de Dominio (Mappers).

4. Capa de Entrada (/app)
Definición de esquemas Pydantic basados en los componentes del YAML (UserPost, ArticlePost, ResponseError).

Manejo de códigos de estado HTTP (201 para creación, 404 para no encontrados).

Reglas de Datos Especiales
Fechas: birthDate se recibe como date en creación, pero los campos de patch y created en artículos usan timestamps en milisegundos (int64).

Relaciones: El campo author en artículos debe ser un UUID válido que exista en la tabla de usuarios.