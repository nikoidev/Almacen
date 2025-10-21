# 🧪 SGA Pro - Testing Manual

## Testing Backend API

### 1. Autenticación

#### Login Admin
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

#### Login Usuario
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user&password=user123"
```

### 2. Productos

#### Listar Productos
```bash
curl -X GET "http://localhost:8000/api/products/" \
  -H "Authorization: Bearer {TOKEN}"
```

#### Crear Producto
```bash
curl -X POST "http://localhost:8000/api/products/" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "PROD-001",
    "name": "Test Product",
    "description": "Product for testing",
    "category": "Electronics",
    "price": 99.99,
    "min_stock_level": 10
  }'
```

### 3. Inventario

#### Ajustar Stock
```bash
curl -X POST "http://localhost:8000/api/inventory/adjust" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "location_id": 1,
    "quantity_change": 100,
    "reason": "Initial stock"
  }'
```

### 4. Dashboard

#### Obtener Resumen
```bash
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "Authorization: Bearer {TOKEN}"
```

### 5. Audit Logs

#### Listar Logs
```bash
curl -X GET "http://localhost:8000/api/audit-logs/" \
  -H "Authorization: Bearer {TOKEN}"
```

## Testing en Swagger

Acceder a: http://localhost:8000/docs

### Checklist de Testing

- [ ] Authentication
  - [ ] Login exitoso
  - [ ] Login fallido (credenciales incorrectas)
  - [ ] Token válido en requests
  
- [ ] Products CRUD
  - [ ] GET /api/products/ (lista)
  - [ ] GET /api/products/{id} (detalle)
  - [ ] POST /api/products/ (crear)
  - [ ] PUT /api/products/{id} (actualizar)
  - [ ] DELETE /api/products/{id} (eliminar)
  
- [ ] Suppliers CRUD
  - [ ] Todas las operaciones CRUD
  
- [ ] Locations CRUD
  - [ ] Todas las operaciones CRUD
  
- [ ] Inventory Operations
  - [ ] GET /api/inventory/ (lista)
  - [ ] GET /api/inventory/product/{id}
  - [ ] POST /api/inventory/adjust
  - [ ] POST /api/inventory/move
  - [ ] GET /api/inventory/low-stock
  
- [ ] Inbound Shipments
  - [ ] POST /api/shipments/ (crear)
  - [ ] GET /api/shipments/ (lista)
  - [ ] GET /api/shipments/{id} (detalle)
  - [ ] POST /api/shipments/{id}/receive
  
- [ ] Outbound Orders
  - [ ] POST /api/orders/ (crear)
  - [ ] GET /api/orders/ (lista)
  - [ ] GET /api/orders/{id} (detalle)
  - [ ] POST /api/orders/{id}/pick
  - [ ] POST /api/orders/{id}/ship
  
- [ ] Dashboard
  - [ ] GET /api/dashboard/summary
  
- [ ] Audit Logs
  - [ ] GET /api/audit-logs/
  - [ ] Verificar logs de operaciones de inventario

## Validaciones a Probar

### Seguridad
- [ ] Endpoints protegidos requieren autenticación
- [ ] Token inválido es rechazado
- [ ] Sin token es rechazado (401)

### Validaciones de Datos
- [ ] Campos requeridos son validados
- [ ] Formatos de datos son validados
- [ ] Registros duplicados son rechazados

### Lógica de Negocio
- [ ] No se permite stock negativo
- [ ] Capacidad de ubicaciones se respeta
- [ ] Stock reservado se maneja correctamente
- [ ] Transacciones son atómicas

### Audit Log
- [ ] Creación de productos se registra
- [ ] Ajustes de inventario se registran
- [ ] Recepciones se registran
- [ ] Salidas se registran
- [ ] Movimientos se registran

## Testing de Transacciones

### Escenario 1: Recepción de Mercancía
1. Crear recepción con items
2. Procesar recepción
3. Verificar que inventario se actualizó
4. Verificar audit log

### Escenario 2: Pedido de Salida
1. Crear pedido con items
2. Verificar que stock se reserva
3. Realizar picking
4. Verificar que stock se reduce
5. Marcar como enviado
6. Verificar audit log

### Escenario 3: Movimiento de Stock
1. Mover stock entre ubicaciones
2. Verificar que cantidad se actualiza en ambas ubicaciones
3. Verificar audit log

## Testing de Errores

- [ ] Producto no existe (404)
- [ ] Datos inválidos (422)
- [ ] Stock insuficiente (400)
- [ ] Ubicación llena (400)
- [ ] Sin autenticación (401)
- [ ] Sin permisos (403)

## Resultados Esperados

✅ Todos los endpoints responden correctamente
✅ Validaciones funcionan como esperado
✅ Audit log registra todas las operaciones
✅ Transacciones son atómicas
✅ Errores se manejan correctamente
✅ Seguridad RBAC funciona

