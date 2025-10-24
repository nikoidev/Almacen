# 🏭 SGA Pro - Sistema de Gestión de Almacenes

[![Backend CI](https://github.com/nikoidev/Almacen/workflows/Backend%20CI/badge.svg)](https://github.com/nikoidev/Almacen/actions)
[![Frontend CI](https://github.com/nikoidev/Almacen/workflows/Frontend%20CI/badge.svg)](https://github.com/nikoidev/Almacen/actions)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.33-black.svg?logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg?logo=postgresql)](https://www.postgresql.org)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB.svg?logo=python)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6.svg?logo=typescript)](https://www.typescriptlang.org)

> **Sistema completo de gestión de almacenes con control de inventario en tiempo real.** Base sólida con gestión de usuarios, roles y permisos (RBAC) + módulos especializados para administración de productos, proveedores, ubicaciones, envíos de entrada/salida, y seguimiento completo de stock con audit log detallado.

---

## ✨ Características Principales

### 🔐 **Autenticación y Seguridad**
- ✅ **JWT con Refresh Tokens** - Tokens de acceso (30 min) y renovación automática (7 días)
- ✅ **Rate Limiting** - Protección contra ataques de fuerza bruta
- ✅ **Recuperación de Contraseña** - Sistema completo vía email con tokens seguros
- ✅ **Cambio de Contraseña** - Con validación de contraseña actual
- ✅ **Validación de Fuerza** - Indicador visual en tiempo real
- ✅ **Encriptación de Datos Sensibles** - Contraseñas SMTP encriptadas con Fernet

### 👥 **Gestión de Usuarios Completa**
- ✅ **CRUD Completo** - Crear, leer, actualizar y eliminar usuarios
- ✅ **Perfil Profesional** - Avatar, teléfono, biografía, zona horaria, idioma
- ✅ **Upload de Avatar** - Con validación de tipo y tamaño (máx 5MB)
- ✅ **Roles Múltiples** - Un usuario puede tener varios roles
- ✅ **Estados** - Activar/desactivar usuarios

### 🛡️ **Sistema RBAC (Role-Based Access Control)**
- ✅ **Roles** - Agrupación de permisos reutilizables
- ✅ **Permisos** - Control granular por recurso y acción
- ✅ **Asignación Dinámica** - Cambios en vivo sin reiniciar

### 📦 **Gestión de Almacén (SGA)**
- ✅ **Productos** - CRUD completo con SKU único, categorías, precios, peso y dimensiones
- ✅ **Proveedores** - Gestión de proveedores con contacto y detalles comerciales
- ✅ **Ubicaciones** - Control de zonas, pasillos, estanterías y niveles con capacidad
- ✅ **Inventario** - Seguimiento de stock en tiempo real por ubicación con stock mínimo
- ✅ **Envíos de Entrada** - Recepción de mercancía con múltiples artículos y actualización automática de stock
- ✅ **Órdenes de Salida** - Proceso completo de picking y despacho con validación de stock
- ✅ **Dashboard Analytics** - Métricas clave, gráficos de tendencias, alertas de stock bajo
- ✅ **Transacciones Atómicas** - Rollback automático en caso de error
- ✅ **Validaciones de Negocio** - Prevención de stock negativo, validación de capacidad

### 📊 **Funcionalidades Avanzadas**
- ✅ **Paginación Inteligente** - 10/25/50/100 items por página
- ✅ **Búsqueda en Tiempo Real** - Con debounce (500ms)
- ✅ **Filtros Múltiples** - Por categoría, proveedor, ubicación, estado de envío/orden
- ✅ **Ordenamiento** - Por cualquier columna (ascendente/descendente)
- ✅ **Audit Log Completo** - Registro de todas las operaciones de inventario con IP y user agent
- ✅ **Historial de Actividad** - Ver últimas acciones de cualquier usuario con detalles completos

### 🎨 **Interfaz Moderna**
- ✅ **Tema Oscuro/Claro** - Toggle persistente
- ✅ **Diseño Responsive** - Mobile, tablet y desktop
- ✅ **Componentes Reutilizables** - Paginación, validación, etc.
- ✅ **Toast Notifications** - Feedback visual inmediato
- ✅ **Iconos** - Heroicons v2

---

## 🏗️ Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────────────────┐
│                            Frontend                                   │
│     Next.js 14 + TypeScript + Tailwind CSS + Recharts                │
│  - Módulos: Dashboard, Inventario, Productos, Proveedores,           │
│    Ubicaciones, Envíos, Órdenes, Usuarios, Roles, Permisos,          │
│    Profile, Audit Logs                                                │
│  - Componentes reutilizables + Context API (Auth, Theme)             │
└────────────────────────────┬─────────────────────────────────────────┘
                             │ HTTP/REST API (JWT Bearer Token)
┌────────────────────────────┴─────────────────────────────────────────┐
│                            Backend                                    │
│            FastAPI + SQLAlchemy + Pydantic + JWT                     │
│  - Autenticación JWT + Refresh Tokens                                │
│  - RBAC (Control de Acceso Basado en Roles)                          │
│  - Servicios: Productos, Proveedores, Ubicaciones, Inventario,       │
│    Envíos, Órdenes, Dashboard, Usuarios, Roles, Audit Log            │
│  - Transacciones atómicas + Validaciones de negocio                  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
┌────────────────────────────┴─────────────────────────────────────────┐
│                         PostgreSQL 15                                 │
│  Tables: users, roles, permissions, user_roles, role_permissions,    │
│          products, suppliers, locations, inventory,                   │
│          inbound_shipments, inbound_shipment_items,                   │
│          outbound_orders, outbound_order_items, audit_logs            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Requisitos Previos

- **Python 3.11+** - [Descargar](https://www.python.org/downloads/)
- **Node.js 18+** - [Descargar](https://nodejs.org/)
- **Docker & Docker Compose** - [Descargar](https://www.docker.com/get-started/)
- **Pipenv** - `pip install pipenv`

---

## 🚀 Instalación Rápida

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/user-management-system.git
cd user-management-system
```

### 2️⃣ Iniciar Base de Datos (PostgreSQL + pgAdmin)

```bash
docker-compose up -d
```

**Accesos:**
- **PostgreSQL**: `localhost:5433`
- **pgAdmin**: `http://localhost:5050`
  - Email: `admin@admin.com`
  - Password: `admin`

### 3️⃣ Configurar Backend

```bash
cd backend

# Instalar dependencias
pipenv install

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus valores

# Ejecutar migraciones
pipenv run python migrate_to_v2.py

# Inicializar datos (usuarios, roles, permisos)
pipenv run python init_db.py

# Iniciar servidor
pipenv run python run.py
```

Backend corriendo en: **http://localhost:8000**  
Documentación API: **http://localhost:8000/docs**

### 4️⃣ Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Construir para producción
npm run build

# Iniciar servidor
npm run start
```

Frontend corriendo en: **http://localhost:3000**

---

## 🔑 Credenciales por Defecto

```
Administrador:
  Usuario: admin
  Contraseña: admin123

Usuario Regular:
  Usuario: user
  Contraseña: user123
```

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción.

---

## 📚 Estructura del Proyecto

```
almacen/
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── api/             # Endpoints REST
│   │   │   ├── routes/      # auth, users, roles, permissions, profile, audit_logs
│   │   │   │                # products, suppliers, locations, inventory
│   │   │   │                # shipments, orders, dashboard
│   │   │   └── deps.py      # Dependencias (auth, db)
│   │   ├── core/            # Configuración central
│   │   │   ├── config.py    # Variables de entorno
│   │   │   ├── security.py  # JWT, hashing
│   │   │   ├── database.py  # SQLAlchemy engine
│   │   │   └── encryption.py # Fernet encryption
│   │   ├── models/          # Modelos SQLAlchemy (14 models)
│   │   ├── schemas/         # Schemas Pydantic (validación)
│   │   ├── services/        # Lógica de negocio (9 services)
│   │   ├── utils/           # Utilidades (audit)
│   │   └── templates/       # Templates HTML para emails
│   ├── uploads/             # Archivos subidos (avatars)
│   ├── Pipfile              # Dependencias Python
│   ├── init_db.py           # Script de inicialización
│   ├── test_api.py          # Script de testing
│   └── run.py               # Entry point
│
├── frontend/                # App Next.js
│   ├── app/                 # App Router
│   │   ├── (protected)/     # Rutas protegidas con Layout
│   │   │   ├── dashboard/       # Dashboard con métricas y gráficos
│   │   │   ├── inventory/       # Vista de inventario
│   │   │   ├── products/        # CRUD productos
│   │   │   ├── suppliers/       # CRUD proveedores
│   │   │   ├── locations/       # CRUD ubicaciones
│   │   │   ├── shipments/       # Envíos de entrada
│   │   │   ├── orders/          # Órdenes de salida
│   │   │   ├── users/           # Gestión de usuarios
│   │   │   ├── roles/           # Gestión de roles
│   │   │   ├── permissions/     # Gestión de permisos
│   │   │   ├── profile/         # Perfil profesional
│   │   │   └── audit-logs/      # Registro de actividad
│   │   └── login/           # Página de inicio de sesión
│   ├── components/          # Componentes reutilizables
│   │   ├── Layout.tsx       # Layout principal con sidebar
│   │   ├── Pagination.tsx   # Componente de paginación
│   │   └── PasswordStrength.tsx # Validador de contraseña
│   ├── contexts/            # React Contexts
│   │   ├── AuthContext.tsx  # Autenticación global
│   │   └── ThemeContext.tsx # Tema oscuro/claro
│   ├── hooks/               # Custom Hooks
│   │   └── useDebounce.ts   # Hook de debounce
│   ├── lib/                 # Utilidades
│   │   ├── api/             # Servicios API (9 services)
│   │   └── axios.ts         # Cliente HTTP con interceptors
│   ├── types/               # TypeScript types
│   └── package.json
│
├── .github/workflows/       # CI/CD con GitHub Actions
│   ├── backend-ci.yml       # Linting, tests, security
│   └── frontend-ci.yml      # Linting, type check, build
│
├── .vscode/                 # Configuración VS Code
│   ├── launch.json          # Debug configs (F5)
│   └── tasks.json           # Tareas automatizadas
│
└── docker-compose.yml       # PostgreSQL + pgAdmin
```

---

## 🔧 Variables de Entorno

### Backend (`.env`)

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/users_db

# Security
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui
SECRET_KEY_ENCRYPTION=clave-fernet-para-encriptacion-32-bytes
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Frontend

No requiere variables de entorno. La URL del backend está configurada en `lib/axios.ts`.

---

## 📖 Uso del Sistema

### Gestión de Usuarios

1. **Crear Usuario**: Click en "Nuevo Usuario" → Rellenar formulario → Asignar roles
2. **Editar Usuario**: Click en ícono de edición → Modificar datos → Guardar
3. **Eliminar Usuario**: Click en ícono de eliminar → Confirmar
4. **Buscar**: Escribir en el campo de búsqueda (busca en nombre, email, username)
5. **Filtrar**: Click en "Filtros" → Seleccionar rol y/o estado
6. **Ordenar**: Click en cualquier header de columna

### Perfil Personal

- **Actualizar Información**: `/profile` → Editar campos → Guardar
- **Cambiar Avatar**: Click en "Cambiar Foto" → Seleccionar imagen → Automático
- **Eliminar Avatar**: Click en "Eliminar Foto"

### Audit Log

- **Ver Actividad**: `/audit-logs` → Lista de todas las acciones
- **Filtrar**: Por acción, recurso, usuario
- **Ver Detalles**: Click en cualquier registro → Modal con información completa

---

## 🔌 API Endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Iniciar sesión | No |
| GET | `/api/auth/me` | Usuario actual | Sí |
| POST | `/api/auth/refresh` | Renovar token | No |
| POST | `/api/auth/forgot-password` | Solicitar recuperación | No |
| POST | `/api/auth/reset-password` | Resetear contraseña | No |
| POST | `/api/auth/change-password` | Cambiar contraseña | Sí |
| POST | `/api/auth/logout` | Cerrar sesión | Sí |

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/users/` | Listar usuarios (paginado) | Sí |
| GET | `/api/users/{id}` | Obtener usuario | Sí |
| POST | `/api/users/` | Crear usuario | Sí |
| PUT | `/api/users/{id}` | Actualizar usuario | Sí |
| DELETE | `/api/users/{id}` | Eliminar usuario | Sí |

### Perfil

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/profile/me` | Obtener mi perfil | Sí |
| PUT | `/api/profile/me` | Actualizar mi perfil | Sí |
| POST | `/api/profile/upload-avatar` | Subir avatar | Sí |
| DELETE | `/api/profile/avatar` | Eliminar avatar | Sí |

### Audit Logs

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/audit-logs/` | Listar logs (paginado) | Sí |
| GET | `/api/audit-logs/recent` | Logs recientes | Sí |
| GET | `/api/audit-logs/my-activity` | Mi actividad | Sí |

### Productos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/products/` | Listar productos (paginado, búsqueda, filtros) | Sí |
| GET | `/api/products/{id}` | Obtener producto | Sí |
| GET | `/api/products/categories` | Listar categorías únicas | Sí |
| POST | `/api/products/` | Crear producto | Sí |
| PUT | `/api/products/{id}` | Actualizar producto | Sí |
| DELETE | `/api/products/{id}` | Eliminar producto | Sí |

### Proveedores

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/suppliers/` | Listar proveedores (paginado) | Sí |
| GET | `/api/suppliers/{id}` | Obtener proveedor | Sí |
| POST | `/api/suppliers/` | Crear proveedor | Sí |
| PUT | `/api/suppliers/{id}` | Actualizar proveedor | Sí |
| DELETE | `/api/suppliers/{id}` | Eliminar proveedor | Sí |

### Ubicaciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/locations/` | Listar ubicaciones (paginado) | Sí |
| GET | `/api/locations/{id}` | Obtener ubicación | Sí |
| GET | `/api/locations/{id}/available-capacity` | Obtener capacidad disponible | Sí |
| POST | `/api/locations/` | Crear ubicación | Sí |
| PUT | `/api/locations/{id}` | Actualizar ubicación | Sí |
| DELETE | `/api/locations/{id}` | Eliminar ubicación | Sí |

### Inventario

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/inventory/` | Listar todo el inventario (paginado) | Sí |
| GET | `/api/inventory/product/{product_id}` | Stock de un producto por ubicación | Sí |
| GET | `/api/inventory/low-stock` | Productos con stock bajo | Sí |
| POST | `/api/inventory/adjust` | Ajustar stock (manual) | Sí |
| POST | `/api/inventory/move` | Mover stock entre ubicaciones | Sí |

### Envíos de Entrada

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/shipments/` | Listar envíos (paginado, filtros) | Sí |
| GET | `/api/shipments/{id}` | Obtener envío con items | Sí |
| POST | `/api/shipments/` | Crear envío de entrada | Sí |
| POST | `/api/shipments/{id}/receive` | Recibir mercancía (actualiza stock) | Sí |
| PUT | `/api/shipments/{id}` | Actualizar envío | Sí |
| DELETE | `/api/shipments/{id}` | Eliminar envío | Sí |

### Órdenes de Salida

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/orders/` | Listar órdenes (paginado, filtros) | Sí |
| GET | `/api/orders/{id}` | Obtener orden con items | Sí |
| POST | `/api/orders/` | Crear orden (reserva stock) | Sí |
| POST | `/api/orders/{id}/pick` | Marcar items como preparados | Sí |
| POST | `/api/orders/{id}/ship` | Enviar orden (reduce stock) | Sí |
| PUT | `/api/orders/{id}` | Actualizar orden | Sí |
| DELETE | `/api/orders/{id}` | Eliminar orden | Sí |

### Dashboard

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/dashboard/summary` | Resumen de métricas y gráficos | Sí |

📖 **Documentación Completa**: http://localhost:8000/docs

---

## 🛠️ Desarrollo

### Backend

```bash
cd backend

# Activar entorno
pipenv shell

# Instalar nueva dependencia
pipenv install nombre-paquete

# Ejecutar tests (cuando se implementen)
pipenv run pytest

# Formatear código
pipenv run black app/

# Linter
pipenv run flake8 app/
```

### Frontend

```bash
cd frontend

# Modo desarrollo (hot reload)
npm run dev

# Build para producción
npm run build

# Iniciar producción
npm run start

# Linter
npm run lint
```

---

## 🚢 Despliegue a Producción

### Checklist Pre-Producción

- [ ] Cambiar `SECRET_KEY` en `.env`
- [ ] Cambiar credenciales de base de datos
- [ ] Cambiar usuarios y contraseñas por defecto
- [ ] Configurar HTTPS (SSL/TLS)
- [ ] Ajustar `CORS_ORIGINS` a dominio de producción
- [ ] Configurar backup automático de base de datos
- [ ] Implementar monitoring (Sentry, NewRelic, etc.)
- [ ] Configurar logs persistentes
- [ ] Revisar rate limits según carga esperada
- [ ] Configurar email SMTP real

### Backend (FastAPI)

```bash
# Usando Gunicorn + Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Frontend (Next.js)

```bash
npm run build
npm run start
```

O despliega en **Vercel** (recomendado para Next.js):
```bash
vercel deploy --prod
```

### Base de Datos

Usa un servicio gestionado como:
- **AWS RDS**
- **Digital Ocean Managed Database**
- **Heroku Postgres**
- **Railway**

---

## 🎯 Casos de Uso

Este sistema sirve como base para:

### ✅ **Sistemas de Gestión Empresarial**
- ERP, CRM, gestión de inventarios
- Control de acceso por departamentos
- Audit log para cumplimiento normativo

### ✅ **E-Commerce**
- Gestión de administradores y vendedores
- Diferentes niveles de acceso (admin, ventas, soporte)
- Registro de todas las operaciones

### ✅ **Sistemas Médicos**
- Control de acceso a historias clínicas
- Diferentes roles (médicos, enfermeras, admin)
- Trazabilidad completa (HIPAA compliance)

### ✅ **Plataformas Educativas**
- Gestión de profesores, estudiantes, administradores
- Permisos por curso/materia
- Registro de actividades académicas

### ✅ **Sistemas de Producción/Manufactura**
- Control de acceso a líneas de producción
- Roles: operadores, supervisores, gerentes
- Audit log de cambios en producción

---

## 🧩 Extensibilidad

### Agregar Nuevos Módulos

1. **Backend**: Crear modelo → schema → servicio → ruta
2. **Frontend**: Crear página → componente → API service
3. **Integrar**: Registrar ruta en `main.py` y link en `Layout.tsx`

### Ejemplo: Agregar módulo de "Productos"

```python
# backend/app/models/product.py
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # ... más campos
```

```typescript
// frontend/app/products/page.tsx
export default function ProductsPage() {
  // Similar estructura a users/page.tsx
}
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: amazing feature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

---

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu@email.com

---

## ⭐ Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework backend moderno y rápido
- [Next.js](https://nextjs.org/) - Framework React para producción
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS utility-first
- [Heroicons](https://heroicons.com/) - Iconos hermosos

---

## 📞 Soporte

¿Problemas o preguntas? 

- 📖 [Wiki](https://github.com/tu-usuario/repo/wiki)
- 🐛 [Issues](https://github.com/tu-usuario/repo/issues)
- 💬 [Discussions](https://github.com/tu-usuario/repo/discussions)

---

<p align="center">
  Hecho con ❤️ para la comunidad Open Source
</p>

<p align="center">
  <strong>⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐</strong>
</p>
