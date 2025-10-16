# 🏭 SGA Pro - Sistema de Gestión de Almacenes

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.33-black.svg?logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg?logo=postgresql)](https://www.postgresql.org)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB.svg?logo=python)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6.svg?logo=typescript)](https://www.typescriptlang.org)

> **Sistema completo de gestión de almacenes (Warehouse Management System - WMS) con control de inventario, recepciones, pedidos, y dashboard con métricas en tiempo real.** Incluye gestión de usuarios, roles y permisos (RBAC), audit log completo, y arquitectura profesional lista para producción.

---

## ✨ Características Principales

### 📦 **Gestión de Almacén**
- ✅ **Control de Inventario** - Stock en tiempo real por producto y ubicación
- ✅ **Gestión de Productos** - Catálogo completo con SKU, categorías, precios
- ✅ **Ubicaciones** - Sistema de códigos (Pasillo-Estante-Sección)
- ✅ **Recepciones de Mercancía** - Inbound con proveedores
- ✅ **Pedidos de Salida** - Outbound con picking y tracking
- ✅ **Movimientos de Stock** - Transferencias entre ubicaciones
- ✅ **Alertas de Bajo Stock** - Notificaciones automáticas

### 📊 **Dashboard y Métricas**
- ✅ **KPIs en Tiempo Real** - Total productos, unidades, valor del inventario
- ✅ **Gráficos Interactivos** - Recharts con barras, circular, líneas
- ✅ **Top Productos** - Ranking por stock, movimientos, valor
- ✅ **Distribución por Categoría** - Visualización de stock
- ✅ **Actividad Reciente** - Entradas vs salidas últimos 30 días

### 🔐 **Autenticación y Seguridad**
- ✅ **JWT con Refresh Tokens** - Sesiones seguras (30 min + renovación 7 días)
- ✅ **RBAC Avanzado** - Control de acceso basado en roles
- ✅ **Rate Limiting** - Protección contra ataques de fuerza bruta
- ✅ **Audit Log Completo** - Registro de todas las operaciones
- ✅ **Encriptación** - Datos sensibles protegidos con Fernet

### 👥 **Gestión de Usuarios**
- ✅ **CRUD Completo** - Crear, leer, actualizar y eliminar usuarios
- ✅ **Perfil Profesional** - Avatar, teléfono, biografía, zona horaria
- ✅ **Roles Múltiples** - Un usuario puede tener varios roles
- ✅ **Estados** - Activar/desactivar usuarios

### 🎨 **Interfaz Moderna**
- ✅ **Tema Oscuro/Claro** - Toggle persistente con transiciones suaves
- ✅ **Diseño Responsive** - Mobile, tablet y desktop
- ✅ **Paginación Inteligente** - 10/25/50/100 items por página
- ✅ **Búsqueda en Tiempo Real** - Con debounce (500ms)
- ✅ **Filtros Múltiples** - Combinables por categoría, estado, rol

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend                                 │
│  Next.js 14 + TypeScript + Tailwind CSS + Recharts              │
│  - Dashboard con gráficos (KPIs, barras, circular)              │
│  - Inventario: Stock en tiempo real                             │
│  - Productos: Catálogo completo                                 │
│  - Recepciones/Pedidos: Gestión de inbound/outbound            │
│  - Usuarios/Roles/Permisos: RBAC                                │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────┴──────────────────────────────────────────┐
│                         Backend                                  │
│          FastAPI + SQLAlchemy + Pydantic + JWT                  │
│  - API RESTful con Swagger docs                                 │
│  - Servicios: Inventory, Products, Orders, Shipments            │
│  - RBAC: Control de permisos granular                           │
│  - Audit Log: Registro completo de operaciones                  │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────────┐
│                       PostgreSQL 15                              │
│  Tables: users, roles, permissions, audit_logs                  │
│          products, inventory, locations, suppliers              │
│          inbound_shipments, outbound_orders                     │
│  Relaciones: user_roles, role_permissions                       │
│  Índices: SKU, location_code, product_id                        │
└─────────────────────────────────────────────────────────────────┘
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
git clone https://github.com/tu-usuario/sga-pro.git
cd sga-pro
```

### 2️⃣ Iniciar Base de Datos (PostgreSQL + pgAdmin)

```bash
docker-compose up -d
```

**Accesos:**
- **PostgreSQL**: `localhost:5438`
- **pgAdmin**: `http://localhost:5058`
  - Email: `admin@admin.com`
  - Password: `admin123`

**Volumen de datos**: Los datos de PostgreSQL y pgAdmin se guardan en `./docker/` (ignorado por git).

**Para reiniciar la BD desde cero**:
```bash
docker-compose down
rm -rf docker/  # o eliminar carpeta manualmente en Windows
docker-compose up -d
```

### 3️⃣ Configurar Backend

```bash
cd backend

# Instalar dependencias con pipenv
pipenv install

# Activar entorno virtual
pipenv shell

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus valores (DATABASE_URL, SECRET_KEY, etc.)

# Inicializar base de datos (crear tablas, permisos, roles, usuarios)
python init_db.py

# Iniciar servidor FastAPI
python run.py
```

**Backend corriendo en**: `http://localhost:8000`  
**Documentación API**: `http://localhost:8000/docs`

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

**Frontend corriendo en**: `http://localhost:3000`

---

## 🔑 Credenciales por Defecto

```
Administrador:
  Usuario: admin
  Contraseña: admin123

Jefe de Almacén:
  Usuario: jefe_almacen
  Contraseña: almacen123

Operario:
  Usuario: operario
  Contraseña: operario123
```

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción.

---

## 📚 Estructura del Proyecto

```
sga-pro/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints REST
│   │   │   ├── routes/
│   │   │   │   ├── auth.py           # Autenticación
│   │   │   │   ├── users.py          # Gestión de usuarios
│   │   │   │   ├── roles.py          # Gestión de roles
│   │   │   │   ├── permissions.py    # Gestión de permisos
│   │   │   │   ├── products.py       # 📦 Catálogo de productos
│   │   │   │   ├── inventory.py      # 📊 Control de inventario
│   │   │   │   ├── locations.py      # 📍 Ubicaciones
│   │   │   │   ├── suppliers.py      # 🏭 Proveedores
│   │   │   │   ├── shipments.py      # 📥 Recepciones
│   │   │   │   ├── orders.py         # 📤 Pedidos
│   │   │   │   ├── dashboard.py      # 📈 Dashboard
│   │   │   │   ├── audit_logs.py     # Registro de actividad
│   │   │   │   └── profile.py        # Perfil de usuario
│   │   │   └── deps.py        # Dependencias (auth, db)
│   │   ├── core/              # Configuración central
│   │   │   ├── config.py      # Variables de entorno
│   │   │   ├── security.py    # JWT, hashing
│   │   │   └── database.py    # SQLAlchemy engine
│   │   ├── models/            # Modelos SQLAlchemy
│   │   │   ├── user.py
│   │   │   ├── role.py
│   │   │   ├── permission.py
│   │   │   ├── product.py              # 📦
│   │   │   ├── supplier.py             # 🏭
│   │   │   ├── location.py             # 📍
│   │   │   ├── inventory.py            # 📊
│   │   │   ├── inbound_shipment.py     # 📥
│   │   │   ├── outbound_order.py       # 📤
│   │   │   └── audit_log.py
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negocio
│   │   │   ├── user_service.py
│   │   │   ├── product_service.py      # 📦
│   │   │   ├── inventory_service.py    # 📊 CORE
│   │   │   ├── shipment_service.py     # 📥
│   │   │   ├── order_service.py        # 📤
│   │   │   └── dashboard_service.py    # 📈
│   │   └── utils/             # Utilidades (audit)
│   ├── uploads/               # Archivos subidos (avatars)
│   ├── Pipfile                # Dependencias Python
│   ├── init_db.py             # Script de inicialización
│   └── run.py                 # Entry point
│
├── frontend/                  # App Next.js
│   ├── app/                   # App Router
│   │   ├── dashboard/         # 📈 Dashboard con gráficos
│   │   ├── inventory/         # 📊 Control de inventario
│   │   ├── products/          # 📦 Gestión de productos
│   │   ├── inbound/           # 📥 Recepciones
│   │   ├── outbound/          # 📤 Pedidos
│   │   ├── users/             # Gestión de usuarios
│   │   ├── roles/             # Gestión de roles
│   │   ├── permissions/       # Gestión de permisos
│   │   ├── profile/           # Perfil profesional
│   │   ├── audit-logs/        # Registro de actividad
│   │   └── login/             # Página de inicio de sesión
│   ├── components/            # Componentes reutilizables
│   │   ├── Layout.tsx         # Layout principal
│   │   ├── Pagination.tsx     # Componente de paginación
│   │   ├── PasswordStrength.tsx # Validador de contraseña
│   │   └── charts/            # 📊 Componentes de gráficos
│   ├── contexts/              # React Contexts
│   │   ├── AuthContext.tsx    # Autenticación global
│   │   └── ThemeContext.tsx   # Tema oscuro/claro
│   ├── hooks/                 # Custom Hooks
│   │   └── useDebounce.ts     # Hook de debounce
│   ├── lib/                   # Utilidades
│   │   ├── api/               # Servicios API
│   │   │   ├── products.ts       # 📦
│   │   │   ├── inventory.ts      # 📊
│   │   │   ├── shipments.ts      # 📥
│   │   │   ├── orders.ts         # 📤
│   │   │   └── dashboard.ts      # 📈
│   │   └── axios.ts           # Cliente HTTP
│   ├── types/                 # TypeScript types
│   └── package.json
│
├── docker-compose.yml         # PostgreSQL + pgAdmin
├── PLAN_DESARROLLO.md         # 📋 Plan detallado fase por fase
└── README.md                  # Este archivo
```

---

## 🔧 Variables de Entorno

### Backend (`.env`)

```env
# Database
DATABASE_URL=postgresql://admin:admin123@localhost:5438/sga_pro_db

# Security
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui
SECRET_KEY_ENCRYPTION=clave-fernet-para-encriptacion-32-bytes
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000

# Email (opcional - para recuperación de contraseña)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-contraseña-encriptada
```

### Frontend

No requiere variables de entorno. La URL del backend está configurada en `lib/axios.ts`.

---

## 📖 Uso del Sistema

### 📦 Gestión de Productos

1. **Crear Producto**: `/products` → "Nuevo Producto" → Rellenar formulario (SKU, nombre, precio, categoría, stock mínimo)
2. **Editar Producto**: Click en ícono de edición → Modificar → Guardar
3. **Eliminar Producto**: Click en ícono de eliminar → Confirmar
4. **Buscar**: Escribir en campo de búsqueda (busca en SKU, nombre, categoría)

### 📊 Control de Inventario

1. **Ver Stock**: `/inventory` → Lista de todo el inventario (producto, ubicación, cantidad)
2. **Mover Stock**: Seleccionar producto → "Mover" → Elegir ubicación destino
3. **Ajustar Stock**: Seleccionar producto → "Ajustar" → Ingresar nueva cantidad
4. **Consultar por Producto**: Buscar SKU → Ver stock en todas las ubicaciones

### 📥 Recepciones de Mercancía

1. **Crear Recepción**: `/inbound` → "Nueva Recepción" → Seleccionar proveedor → Añadir productos esperados
2. **Procesar Recepción**: Click en recepción pendiente → Ingresar cantidades recibidas → "Completar"
3. **Ver Historial**: Lista de todas las recepciones con filtros por estado

### 📤 Pedidos de Salida

1. **Crear Pedido**: `/outbound` → "Nuevo Pedido" → Ingresar cliente → Añadir productos
2. **Realizar Picking**: Click en pedido → "Iniciar Picking" → Confirmar cantidades → "Completar"
3. **Marcar Enviado**: Click en pedido empacado → "Marcar como Enviado"

### 📈 Dashboard

- **KPIs**: Visualiza totales de productos, unidades, valor del inventario
- **Gráficos**: Barras (top productos), circular (distribución), líneas (actividad)
- **Alertas**: Lista de productos con bajo stock que requieren reabastecimiento

### 👥 Gestión de Usuarios

1. **Crear Usuario**: `/users` → "Nuevo Usuario" → Asignar roles (Operario, Jefe de Almacén, Admin)
2. **Editar Usuario**: Click en ícono de edición → Modificar roles/permisos
3. **Activar/Desactivar**: Toggle de estado activo

---

## 🔌 API Endpoints

### 📦 Productos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/products/` | Listar productos (paginado) | Sí |
| GET | `/api/products/{id}` | Obtener producto | Sí |
| POST | `/api/products/` | Crear producto | Sí |
| PUT | `/api/products/{id}` | Actualizar producto | Sí |
| DELETE | `/api/products/{id}` | Eliminar producto | Sí |

### 📊 Inventario

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/inventory/` | Consultar inventario | Sí |
| GET | `/api/inventory/product/{id}` | Stock por producto | Sí |
| POST | `/api/inventory/adjust` | Ajustar stock | Sí |
| POST | `/api/inventory/move` | Mover stock | Sí |

### 📥 Recepciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/shipments/` | Listar recepciones | Sí |
| POST | `/api/shipments/` | Crear recepción | Sí |
| POST | `/api/shipments/{id}/receive` | Procesar recepción | Sí |

### 📤 Pedidos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/orders/` | Listar pedidos | Sí |
| POST | `/api/orders/` | Crear pedido | Sí |
| POST | `/api/orders/{id}/pick` | Realizar picking | Sí |
| POST | `/api/orders/{id}/ship` | Marcar como enviado | Sí |

### 📈 Dashboard

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/dashboard/summary` | Métricas y KPIs | Sí |

📖 **Documentación Completa**: http://localhost:8000/docs

---

## 🛡️ Sistema de Permisos

### Roles Predefinidos

#### 👨‍💼 Administrador
- Acceso total al sistema
- Gestión de usuarios, roles y permisos
- Todas las operaciones de almacén

#### 🏭 Jefe de Almacén
- Gestión completa de almacén
- Crear productos, proveedores, ubicaciones
- Procesar recepciones y pedidos
- Ver dashboard con métricas

#### 📦 Operario de Almacén
- Consultar inventario
- Procesar recepciones
- Realizar picking de pedidos
- Sin acceso a creación de productos

### Permisos Granulares

```
product:create, product:read, product:update, product:delete
inventory:read, inventory:move, inventory:adjust
shipment:create, shipment:read, shipment:receive
order:create, order:read, order:pick, order:ship
dashboard:view
user:create, user:read, user:update, user:delete
role:create, role:read, role:update, role:delete
```

---

## 🛠️ Desarrollo

### Backend

```bash
cd backend

# Activar entorno virtual
pipenv shell

# Instalar nueva dependencia
pipenv install nombre-paquete

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

O despliega en **Vercel** (recomendado):
```bash
vercel deploy --prod
```

---

## 🎯 Casos de Uso

### ✅ **Almacenes y Centros de Distribución**
- Control de inventario en tiempo real
- Gestión de múltiples ubicaciones
- Tracking de recepciones y despachos
- Alertas de reabastecimiento

### ✅ **E-Commerce**
- Integración con tienda online
- Gestión de pedidos y fulfillment
- Control de stock por canal
- Dashboard con métricas de ventas

### ✅ **Manufactura**
- Control de materias primas
- Gestión de productos terminados
- Trazabilidad completa
- Integración con producción

### ✅ **Distribución**
- Gestión de proveedores
- Control de múltiples almacenes
- Optimización de rutas de picking
- Análisis de rotación de inventario

---

## 📊 Tecnologías Utilizadas

### Backend
- **FastAPI** 0.115.0 - Framework web moderno y rápido
- **SQLAlchemy** 2.0.36 - ORM para Python
- **PostgreSQL** 15 - Base de datos relacional
- **Pydantic** 2.10.0 - Validación de datos
- **JWT** - Autenticación con tokens
- **Bcrypt** - Hashing de contraseñas

### Frontend
- **Next.js** 14.2.33 - Framework React para producción
- **TypeScript** 5.2.2 - JavaScript con tipos
- **Tailwind CSS** 3.3.5 - Framework CSS utility-first
- **Recharts** - Librería de gráficos
- **Axios** - Cliente HTTP
- **Heroicons** - Iconos SVG

---

## 📈 Roadmap

### Fase 1: Core (Completado)
- [x] Sistema de usuarios, roles y permisos
- [x] Autenticación JWT
- [x] Audit log

### Fase 2: Almacén Básico (En Desarrollo)
- [ ] Gestión de productos
- [ ] Control de inventario
- [ ] Ubicaciones
- [ ] Dashboard básico

### Fase 3: Operaciones (Planeado)
- [ ] Recepciones de mercancía
- [ ] Pedidos de salida
- [ ] Movimientos de stock
- [ ] Alertas automáticas

### Fase 4: Analytics (Futuro)
- [ ] Reportes avanzados
- [ ] Predicción de demanda
- [ ] Optimización de stock
- [ ] Exportación de datos (CSV, Excel, PDF)

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: amazing feature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver `CONTRIBUTING.md` para más detalles.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

---

## 👨‍💻 Equipo

**Desarrolladores**
- GitHub: [@nikoidev](https://github.com/nikoidev)

---

## 📞 Soporte

¿Problemas o preguntas? 

- 📖 [Documentación](PLAN_DESARROLLO.md)
- 🐛 [Issues](https://github.com/nikoidev/sga-pro/issues)
- 💬 [Discussions](https://github.com/nikoidev/sga-pro/discussions)

---

## ⭐ Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework backend moderno y rápido
- [Next.js](https://nextjs.org/) - Framework React para producción
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS utility-first
- [Recharts](https://recharts.org/) - Librería de gráficos para React
- [Heroicons](https://heroicons.com/) - Iconos hermosos

---

<p align="center">
  <strong>📦 SGA Pro - Tu solución completa de gestión de almacenes 📦</strong>
</p>

<p align="center">
  Hecho con ❤️ para la comunidad Open Source
</p>

<p align="center">
  <strong>⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐</strong>
</p>
