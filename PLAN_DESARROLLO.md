# 📋 Plan de Desarrollo - SGA Pro (Sistema de Gestión de Almacenes)

## 🎯 Objetivo Principal

Extender el "Sistema de Gestión de Usuarios Universal" existente para convertirlo en un Sistema de Gestión de Almacenes (SGA) completamente funcional llamado **"SGA Pro"**. Integraremos los nuevos módulos de almacén de forma nativa, aprovechando la infraestructura de usuarios, roles, permisos y arquitectura ya establecida.

---

## 🏗️ Principios y Buenas Prácticas

### DRY (Don't Repeat Yourself)
- ✅ Crear servicios, componentes y utilidades reutilizables
- ✅ Evitar duplicación de código en backend y frontend

### Código Limpio y Modular
- ✅ Estructura intuitiva con responsabilidades claras
- ✅ Separación: modelos, servicios, rutas (backend) | componentes, páginas, APIs (frontend)

### Seguridad Integrada
- ✅ Todas las rutas API protegidas con RBAC
- ✅ Control de acceso por permisos

### Rendimiento
- ✅ Consultas a base de datos eficientes
- ✅ Frontend rápido y responsivo con Next.js

### Mantenibilidad
- ✅ Código bien comentado (especialmente lógica de negocio)
- ✅ Fácil de entender y extender

---

## 📊 Configuración del Entorno

### Docker Compose
- **Base de datos**: `sga_pro_db`
- **PostgreSQL**: Puerto `5438`
- **pgAdmin**: Puerto `5058`
- **Volumen**: `sga_postgres_data`

### Backend
- **Entorno virtual**: pipenv
- **Python**: 3.13
- **Framework**: FastAPI 0.115.0

### Frontend
- **Framework**: Next.js 14.2.33
- **TypeScript**: 5.2.2
- **Nueva dependencia**: recharts (para gráficos)

---

## 🗂️ Modelos de Base de Datos

### 1. Product (Producto)
```python
- id: Integer (PK)
- sku: String (único, indexado)
- name: String
- description: Text
- category: String (para agrupación en dashboard)
- price: Decimal
- min_stock_level: Integer (para alertas)
- created_at: DateTime
- updated_at: DateTime
```

### 2. Supplier (Proveedor)
```python
- id: Integer (PK)
- name: String
- contact_person: String
- email: String
- phone: String
- address: Text
- created_at: DateTime
- updated_at: DateTime
```

### 3. Location (Ubicación)
```python
- id: Integer (PK)
- code: String (ej: "A1-R2-S3", único)
- description: String (ej: "Pasillo 1, Estante 2")
- capacity: Integer (capacidad máxima)
- created_at: DateTime
```

### 4. Inventory (Inventario)
```python
- id: Integer (PK)
- product_id: Integer (FK → Product)
- location_id: Integer (FK → Location)
- quantity: Integer
- reserved_quantity: Integer (stock comprometido)
- last_updated: DateTime
- CONSTRAINT: unique(product_id, location_id)
```

### 5. InboundShipment (Recepción de Mercancía)
```python
- id: Integer (PK)
- supplier_id: Integer (FK → Supplier)
- status: Enum ("PENDIENTE", "EN_PROCESO", "COMPLETADO")
- expected_at: DateTime
- received_at: DateTime (nullable)
- created_at: DateTime
```

### 6. InboundShipmentItem (Detalle de Recepción)
```python
- id: Integer (PK)
- shipment_id: Integer (FK → InboundShipment)
- product_id: Integer (FK → Product)
- quantity_expected: Integer
- quantity_received: Integer
- location_id: Integer (FK → Location)
```

### 7. OutboundOrder (Pedido de Salida)
```python
- id: Integer (PK)
- customer_name: String
- status: Enum ("PENDIENTE", "EN_PICKING", "EMPACADO", "ENVIADO")
- created_at: DateTime
- shipped_at: DateTime (nullable)
```

### 8. OutboundOrderItem (Detalle de Pedido)
```python
- id: Integer (PK)
- order_id: Integer (FK → OutboundOrder)
- product_id: Integer (FK → Product)
- quantity_ordered: Integer
- quantity_picked: Integer
- location_id: Integer (FK → Location)
```

---

## 🔐 Sistema de Permisos RBAC

### Nuevos Permisos a Crear

#### Productos
- `product:create` - Crear productos
- `product:read` - Ver productos
- `product:update` - Actualizar productos
- `product:delete` - Eliminar productos

#### Inventario
- `inventory:read` - Consultar inventario
- `inventory:move` - Mover stock entre ubicaciones
- `inventory:adjust` - Ajustar cantidades manualmente

#### Recepciones
- `shipment:create` - Crear recepciones
- `shipment:read` - Ver recepciones
- `shipment:receive` - Procesar recepción de mercancía

#### Pedidos
- `order:create` - Crear pedidos de salida
- `order:read` - Ver pedidos
- `order:pick` - Realizar picking
- `order:ship` - Marcar como enviado

#### Dashboard
- `dashboard:view` - Ver dashboard con métricas

### Nuevos Roles a Crear

#### Operario de Almacén
Permisos asignados:
- `product:read`
- `inventory:read`
- `shipment:receive`
- `order:pick`

#### Jefe de Almacén
Permisos asignados:
- Todos los permisos de Operario
- `product:create`, `product:update`
- `inventory:move`, `inventory:adjust`
- `shipment:create`
- `order:create`, `order:ship`
- `dashboard:view`

---

## 📅 Plan de Ejecución por Fases

### ✅ **FASE 0: Configuración Inicial** (Completada)
- [x] Actualizar `docker-compose.yml` con nuevos servicios
- [x] Cambiar nombre de BD a `sga_pro_db`
- [x] Puertos: PostgreSQL `5438`, pgAdmin `5058`
- [x] Crear `PLAN_DESARROLLO.md`
- [x] Actualizar `README.md`
- [x] Actualizar `backend/app/main.py`
- [x] Configurar pipenv (entorno virtual: `backend-gqFweA_L`)
- [x] Levantar contenedores Docker

---

### ✅ **FASE 1: Base de Datos** (COMPLETADA)

#### Backend - Modelos ✅
- [x] Crear `backend/app/models/product.py`
- [x] Crear `backend/app/models/supplier.py`
- [x] Crear `backend/app/models/location.py`
- [x] Crear `backend/app/models/inventory.py`
- [x] Crear `backend/app/models/inbound_shipment.py` (incluye InboundShipmentItem)
- [x] Crear `backend/app/models/outbound_order.py` (incluye OutboundOrderItem)
- [x] Actualizar `backend/app/models/__init__.py`
- [x] Crear tablas en la base de datos (14 tablas totales)

#### Backend - Schemas Pydantic ✅
- [x] Crear `backend/app/schemas/product.py`
- [x] Crear `backend/app/schemas/supplier.py`
- [x] Crear `backend/app/schemas/location.py`
- [x] Crear `backend/app/schemas/inventory.py`
- [x] Crear `backend/app/schemas/shipment.py`
- [x] Crear `backend/app/schemas/order.py`
- [x] Actualizar `backend/app/schemas/__init__.py`

#### Inicialización ✅
- [x] Actualizar `backend/init_db.py` con nuevos permisos y roles
- [x] Ejecutar migraciones
- [x] Verificar tablas en pgAdmin
- [x] Base de datos inicializada con usuarios admin/user

---

### ✅ **FASE 2: Backend - Servicios** (COMPLETADA)

- [x] Crear `backend/app/services/product_service.py`
  - CRUD completo
  - Búsqueda y filtros
  
- [x] Crear `backend/app/services/supplier_service.py`
  - CRUD completo
  
- [x] Crear `backend/app/services/location_service.py`
  - CRUD completo
  - Validar capacidad
  
- [x] Crear `backend/app/services/inventory_service.py` ⭐ **CORE**
  - `add_stock(product_id, location_id, quantity, user_id)`
  - `remove_stock(product_id, location_id, quantity, user_id)`
  - `move_stock(product_id, from_location, to_location, quantity)`
  - `get_stock_level(product_id, location_id=None)`
  - `get_low_stock_products()`
  - Validaciones: no stock negativo, capacidad de ubicación
  - Audit log automático en cada operación

---

### ✅ **FASE 3: Backend - API Endpoints (CRUD Básico)** (COMPLETADA)

- [x] Crear `backend/app/api/routes/products.py`
  - GET `/api/products/` (lista con paginación, búsqueda, filtros)
  - GET `/api/products/{id}` (detalle)
  - POST `/api/products/` (crear)
  - PUT `/api/products/{id}` (actualizar)
  - DELETE `/api/products/{id}` (eliminar)
  
- [x] Crear `backend/app/api/routes/suppliers.py`
  - CRUD completo similar a products
  
- [x] Crear `backend/app/api/routes/locations.py`
  - CRUD completo
  
- [x] Crear `backend/app/api/routes/inventory.py`
  - GET `/api/inventory/` (consulta de stock)
  - GET `/api/inventory/product/{id}` (stock por producto)
  - POST `/api/inventory/adjust` (ajuste manual)
  - POST `/api/inventory/move` (mover stock)
  
- [x] Registrar routers en `backend/app/main.py`

---

### ✅ **FASE 4: Backend - Operaciones de Almacén** (COMPLETADA)

- [x] Crear `backend/app/services/shipment_service.py`
  - Crear recepción
  - Procesar recepción (actualiza inventario)
  - Cambiar estado
  
- [x] Crear `backend/app/api/routes/shipments.py`
  - POST `/api/shipments/` (crear recepción)
  - GET `/api/shipments/` (lista)
  - GET `/api/shipments/{id}` (detalle)
  - POST `/api/shipments/{id}/receive` (procesar recepción)
  
- [x] Crear `backend/app/services/order_service.py`
  - Crear pedido
  - Realizar picking (reduce inventario)
  - Cambiar estado
  
- [x] Crear `backend/app/api/routes/orders.py`
  - POST `/api/orders/` (crear pedido)
  - GET `/api/orders/` (lista)
  - GET `/api/orders/{id}` (detalle)
  - POST `/api/orders/{id}/pick` (realizar picking)
  - POST `/api/orders/{id}/ship` (marcar como enviado)

---

### ✅ **FASE 5: Backend - Dashboard** (COMPLETADA)

- [x] Crear `backend/app/schemas/dashboard.py`
  - DashboardSummary, StockByCategory, TopProduct
  - LowStockAlert, MovementData, WarehouseUtilization
  
- [x] Crear `backend/app/services/dashboard_service.py`
  - `get_summary()` con métricas agregadas:
    - `total_products`: Conteo de productos
    - `total_stock_units`: Suma de unidades en inventario
    - `total_stock_value`: Suma de (quantity * price)
    - `low_stock_products`: Lista de productos bajo umbral
    - `stock_by_category`: Agrupación por categoría
    - `movements_last_30_days`: Recepciones vs salidas (30 días)
    - `top_products_by_stock`: Top 5 productos con más stock
    - `warehouse_utilization`: Capacidad ocupada vs total
  
- [x] Crear `backend/app/api/routes/dashboard.py`
  - GET `/api/dashboard/summary`
  
- [x] Registrar router en `main.py`
- [x] Actualizar __init__.py en schemas y services

---

### ✅ **FASE 6: Frontend - Dependencias** (COMPLETADA)

- [x] Actualizar `frontend/package.json`:
  ```bash
  npm install recharts
  npm install @types/recharts --save-dev
  ```
- [x] Instalado `recharts ^3.2.1` (gráficos)
- [x] Instalado `@types/recharts ^1.8.29` (tipos TypeScript)

---

### ✅ **FASE 7: Frontend - Types y API Services** (COMPLETADA)

- [x] Actualizar `frontend/types/index.ts` con nuevos tipos:
  - `Product`, `ProductCreate`, `ProductUpdate`
  - `Supplier`, `SupplierCreate`, `SupplierUpdate`
  - `Location`, `LocationCreate`, `LocationUpdate`
  - `Inventory`, `InventoryAdjust`, `InventoryMove`, `InventoryByProduct`
  - `InboundShipment`, `InboundShipmentCreate`, `InboundShipmentReceive`
  - `OutboundOrder`, `OutboundOrderCreate`, `OutboundOrderPick`
  - `DashboardSummary` con todos sus sub-tipos
  - Enums: `ShipmentStatus`, `OrderStatus`

- [x] Crear `frontend/lib/api/products.ts` (CRUD + getCategories)
- [x] Crear `frontend/lib/api/suppliers.ts` (CRUD completo)
- [x] Crear `frontend/lib/api/locations.ts` (CRUD + getAvailableCapacity)
- [x] Crear `frontend/lib/api/inventory.ts` (getAll, getByProduct, getLowStock, adjust, move)
- [x] Crear `frontend/lib/api/shipments.ts` (CRUD + receive)
- [x] Crear `frontend/lib/api/orders.ts` (CRUD + pick + ship)
- [x] Crear `frontend/lib/api/dashboard.ts` (getSummary)

---

### ✅ **FASE 8: Frontend - Layout y Navegación** (COMPLETADA)

- [x] Actualizar `frontend/components/Layout.tsx`
  - [x] Cambiar nombre a "SGA Pro - Sistema de Gestión de Almacenes"
  - [x] Organizar navegación por secciones:
    - **Dashboard**: Inicio (con gráficos)
    - **Gestión de Almacén**: Inventario, Productos, Proveedores, Ubicaciones, Recepciones, Pedidos
    - **Administración**: Usuarios, Roles, Permisos, Actividad
  - [x] Agregar iconos de Heroicons:
    - ChartBarIcon (Dashboard)
    - ArchiveBoxIcon (Inventario)
    - CubeIcon (Productos)
    - BuildingStorefrontIcon (Proveedores)
    - MapPinIcon (Ubicaciones)
    - ArrowDownTrayIcon (Recepciones)
    - ArrowUpTrayIcon (Pedidos)
  - [x] Mantener perfil de usuario y logout

---

### **FASE 9: Frontend - Vistas CRUD Básicas** (Día 12-13)

- [ ] Crear `frontend/app/products/page.tsx`
  - Lista de productos con tabla
  - Paginación, búsqueda, filtros
  - Modal para crear/editar
  - Botón eliminar con confirmación
  
- [ ] Crear `frontend/app/suppliers/page.tsx`
  - Similar a products
  
- [ ] Crear `frontend/app/locations/page.tsx`
  - Similar a products
  
- [ ] Crear `frontend/app/inventory/page.tsx`
  - Tabla de inventario (producto, ubicación, cantidad)
  - Búsqueda por SKU o nombre
  - Botones: "Mover Stock", "Ajustar"
  - Modales para operaciones

---

### **FASE 10: Frontend - Operaciones de Almacén** (Día 14-15)

- [ ] Crear `frontend/app/inbound/page.tsx`
  - Lista de recepciones
  - Modal para crear nueva recepción
  - Vista de detalle con items
  - Botón "Procesar Recepción"
  
- [ ] Crear `frontend/app/outbound/page.tsx`
  - Lista de pedidos
  - Modal para crear nuevo pedido
  - Vista de detalle con items
  - Botones: "Realizar Picking", "Marcar Enviado"

---

### **FASE 11: Frontend - Dashboard con Gráficos** (Día 16-17)

- [ ] Actualizar `frontend/app/dashboard/page.tsx`
  
#### KPIs (Tarjetas superiores)
  - Total de Productos
  - Unidades en Stock
  - Valor del Inventario
  - Productos con Bajo Stock

#### Gráficos (usando recharts)
  - **Gráfico de Barras**: Top 5 Productos por Stock
  - **Gráfico Circular**: Distribución de Stock por Categoría
  - **Gráfico de Línea**: Movimientos últimos 30 días (Entradas vs Salidas)

#### Tabla
  - Productos con Bajo Stock (alertas)
  
- [ ] Crear componentes reutilizables:
  - `frontend/components/charts/BarChartComponent.tsx`
  - `frontend/components/charts/PieChartComponent.tsx`
  - `frontend/components/charts/LineChartComponent.tsx`
  - `frontend/components/KPICard.tsx`

---

### **FASE 12: Testing y Refinamiento** (Día 18-19)

#### Backend
- [ ] Probar todos los endpoints en Swagger (`/docs`)
- [ ] Verificar audit logs en recepciones y salidas
- [ ] Probar transacciones (mover stock debe ser atómico)
- [ ] Verificar permisos RBAC en cada ruta

#### Frontend
- [ ] Build de producción: `npm run build`
- [ ] Revisar linter: `npm run lint`
- [ ] Probar todas las vistas en móvil y desktop
- [ ] Verificar modo oscuro/claro
- [ ] Validar formularios
- [ ] Probar operaciones de inventario

#### Integración
- [ ] Crear usuario "Operario" y verificar permisos limitados
- [ ] Crear usuario "Jefe de Almacén" y verificar permisos completos
- [ ] Verificar que audit log registra todas las operaciones

---

### **FASE 13: Documentación** (Día 20)

- [ ] Actualizar `README.md` con:
  - Nuevas funcionalidades del SGA
  - Screenshots del dashboard
  - Guía de uso del sistema de almacén
  
- [ ] Actualizar `CONTRIBUTING.md` si aplica

- [ ] Crear `docs/API.md` con documentación de nuevos endpoints

- [ ] Crear `docs/PERMISOS.md` con matriz de permisos

---

## 📈 Métricas de Éxito

- ✅ Todas las operaciones CRUD funcionan
- ✅ Dashboard muestra métricas en tiempo real
- ✅ Audit log registra todas las operaciones de inventario
- ✅ Sistema RBAC controla acceso correctamente
- ✅ Frontend responsive y rápido
- ✅ Build de producción sin errores
- ✅ Documentación actualizada

---

## 🚀 Comandos Útiles

### Iniciar Proyecto
```bash
# Levantar base de datos
docker-compose up -d

# Backend (en /backend)
pipenv install
pipenv shell
python init_db.py
python run.py

# Frontend (en /frontend)
npm install
npm run dev
```

### Desarrollo
```bash
# Ver logs de Docker
docker-compose logs -f

# Acceder a pgAdmin
http://localhost:5058

# Ver API docs
http://localhost:8000/docs

# Frontend
http://localhost:3000
```

---

## 📝 Notas Importantes

### Transacciones Atómicas
Todas las operaciones de inventario deben ser atómicas (usar `db.commit()` y `db.rollback()`).

### Validaciones Críticas
- No permitir stock negativo
- Validar capacidad de ubicaciones
- Validar que existan productos/ubicaciones antes de operar

### Audit Log
Registrar automáticamente:
- Creación de productos
- Recepciones de mercancía
- Salidas de mercancía
- Movimientos de stock
- Ajustes manuales

### Performance
- Usar índices en columnas frecuentes (sku, location_code)
- Cachear métricas del dashboard si es necesario
- Paginar todas las listas

---

## 🎯 Estado Actual

**Fase Actual**: ✅ **FASE 0-8 COMPLETADAS** | 🚧 **FASE 9: Frontend - Vistas CRUD** (Siguiente)

### ✅ Backend Completado (100%)
- **14 tablas** en base de datos funcionando
- **7 módulos de servicios** con lógica de negocio completa (incluye Dashboard)
- **7 routers de API** con todos los endpoints CRUD + Analytics
- **Schemas Pydantic** validados
- **Base de datos** inicializada con usuarios y permisos
- **CI/CD** configurado (GitHub Actions)
- **VS Code** launch.json configurado
- **Docker** funcionando (PostgreSQL 5438, pgAdmin 5058)

### 📊 API Endpoints Disponibles
- ✅ `/api/products/` - Gestión de productos
- ✅ `/api/suppliers/` - Gestión de proveedores
- ✅ `/api/locations/` - Gestión de ubicaciones
- ✅ `/api/inventory/` - Control de inventario
- ✅ `/api/shipments/` - Recepciones de mercancía
- ✅ `/api/orders/` - Pedidos de salida
- ✅ `/api/dashboard/summary` - Métricas y Analytics ⭐ **NUEVO**

### 🔐 Usuarios Creados
- **admin / admin123** (Administrador completo)
- **user / user123** (Usuario básico)

### 🎯 Próximas Fases
1. **FASE 9**: Frontend - Vistas CRUD (Productos, Proveedores, Ubicaciones) 🎯 **← Siguiente**
2. **FASE 10**: Frontend - Vista de Inventario y Operaciones
3. **FASE 11**: Frontend - Dashboard con gráficos (Recharts)
4. **FASE 12-13**: Testing, refinamiento y documentación

### 📦 Frontend - Completado
- ✅ **Types**: 277 líneas de interfaces TypeScript
- ✅ **API Services**: 7 módulos completos
- ✅ **Layout**: Navegación organizada en 3 secciones con 11 enlaces
- ✅ **Iconos**: Heroicons integrados para cada módulo
- ✅ **Dependencias**: recharts ^3.2.1, @types/recharts ^1.8.29

---

**Fecha de Inicio**: 16/10/2025  
**Última Actualización**: 16/10/2025 - 15:45

