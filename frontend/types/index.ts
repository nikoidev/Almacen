export interface User {
  id: number
  email: string
  username: string
  first_name?: string
  last_name?: string
  is_active: boolean
  is_superuser: boolean
  phone?: string
  avatar_url?: string
  bio?: string
  timezone?: string
  language?: string
  created_at: string
  updated_at?: string
  roles: Role[]
}

export interface Role {
  id: number
  name: string
  description?: string
  is_active: boolean
  created_at: string
  updated_at?: string
  permissions: Permission[]
}

export interface Permission {
  id: number
  name: string
  code: string
  description?: string
  resource?: string
  action?: string
  is_active: boolean
  created_at: string
  updated_at?: string
}

export interface UserCreate {
  email: string
  username: string
  password: string
  first_name?: string
  last_name?: string
  is_active?: boolean
  role_ids?: number[]
}

export interface UserUpdate {
  email?: string
  username?: string
  password?: string
  first_name?: string
  last_name?: string
  is_active?: boolean
  role_ids?: number[]
}

export interface RoleCreate {
  name: string
  description?: string
  is_active?: boolean
  permission_ids?: number[]
}

export interface RoleUpdate {
  name?: string
  description?: string
  is_active?: boolean
  permission_ids?: number[]
}

export interface PermissionCreate {
  name: string
  code: string
  description?: string
  resource?: string
  action?: string
  is_active?: boolean
}

export interface PermissionUpdate {
  name?: string
  code?: string
  description?: string
  resource?: string
  action?: string
  is_active?: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pages: number
  limit: number
}

export interface Token {
  access_token: string
  token_type: string
  refresh_token?: string
}

export interface AuditLog {
  id: number
  user_id?: number
  action: string
  resource: string
  resource_id?: number
  details?: any
  ip_address?: string
  user_agent?: string
  created_at: string
  user_username?: string
  user_email?: string
}

export interface ProfileUpdate {
  first_name?: string
  last_name?: string
  phone?: string
  avatar_url?: string
  bio?: string
  timezone?: string
  language?: string
}

// ============================================
// SGA (Warehouse Management System) Types
// ============================================

// Product Types
export interface Product {
  id: number
  sku: string
  name: string
  description?: string
  category?: string
  price: number
  min_stock_level: number
  created_at: string
  updated_at?: string
}

export interface ProductCreate {
  sku: string
  name: string
  description?: string
  category?: string
  price: number
  min_stock_level?: number
}

export interface ProductUpdate {
  sku?: string
  name?: string
  description?: string
  category?: string
  price?: number
  min_stock_level?: number
}

// Supplier Types
export interface Supplier {
  id: number
  name: string
  contact_person?: string
  email?: string
  phone?: string
  address?: string
  created_at: string
  updated_at?: string
}

export interface SupplierCreate {
  name: string
  contact_person?: string
  email?: string
  phone?: string
  address?: string
}

export interface SupplierUpdate {
  name?: string
  contact_person?: string
  email?: string
  phone?: string
  address?: string
}

// Location Types
export interface Location {
  id: number
  code: string
  description?: string
  capacity: number
  created_at: string
  updated_at?: string
}

export interface LocationCreate {
  code: string
  description?: string
  capacity: number
}

export interface LocationUpdate {
  code?: string
  description?: string
  capacity?: number
}

// Inventory Types
export interface Inventory {
  id: number
  product_id: number
  location_id: number
  quantity: number
  reserved_quantity: number
  last_updated: string
  product?: Product
  location?: Location
}

export interface InventoryAdjust {
  product_id: number
  location_id: number
  quantity_change: number
  reason: string
}

export interface InventoryMove {
  product_id: number
  from_location_id: number
  to_location_id: number
  quantity: number
}

export interface InventoryByProduct {
  product_id: number
  product_sku: string
  product_name: string
  locations: Array<{
    location_id: number
    location_code: string
    quantity: number
    reserved_quantity: number
  }>
  total_quantity: number
  total_reserved: number
  available_quantity: number
}

export interface LowStockProduct {
  product_id: number
  sku: string
  name: string
  current_stock: number
  min_stock_level: number
  difference: number
}

// Inbound Shipment Types
export enum ShipmentStatus {
  PENDING = 'PENDING',
  IN_PROCESS = 'IN_PROCESS',
  COMPLETED = 'COMPLETED'
}

export interface InboundShipmentItem {
  id: number
  shipment_id: number
  product_id: number
  quantity_expected: number
  quantity_received: number
  location_id: number
  product?: Product
  location?: Location
}

export interface InboundShipment {
  id: number
  supplier_id: number
  status: ShipmentStatus
  expected_at: string
  received_at?: string
  created_at: string
  supplier?: Supplier
  items: InboundShipmentItem[]
}

export interface InboundShipmentCreate {
  supplier_id: number
  expected_at: string
  items: Array<{
    product_id: number
    quantity_expected: number
    location_id: number
  }>
}

export interface InboundShipmentReceive {
  items: Array<{
    item_id: number
    quantity_received: number
  }>
}

// Outbound Order Types
export enum OrderStatus {
  PENDING = 'PENDING',
  IN_PICKING = 'IN_PICKING',
  PACKED = 'PACKED',
  SHIPPED = 'SHIPPED'
}

export interface OutboundOrderItem {
  id: number
  order_id: number
  product_id: number
  quantity_ordered: number
  quantity_picked: number
  location_id: number
  product?: Product
  location?: Location
}

export interface OutboundOrder {
  id: number
  customer_name: string
  status: OrderStatus
  created_at: string
  shipped_at?: string
  items: OutboundOrderItem[]
}

export interface OutboundOrderCreate {
  customer_name: string
  items: Array<{
    product_id: number
    quantity_ordered: number
    location_id: number
  }>
}

export interface OutboundOrderPick {
  items: Array<{
    item_id: number
    quantity_picked: number
  }>
}

// Dashboard Types
export interface StockByCategory {
  category: string
  total_units: number
  total_value: number
}

export interface TopProduct {
  product_id: number
  sku: string
  name: string
  total_stock: number
  total_value: number
}

export interface LowStockAlert {
  product_id: number
  sku: string
  name: string
  current_stock: number
  min_stock_level: number
  difference: number
}

export interface MovementData {
  date: string
  inbound: number
  outbound: number
}

export interface WarehouseUtilization {
  total_capacity: number
  occupied_units: number
  utilization_percentage: number
  available_capacity: number
}

export interface DashboardSummary {
  total_products: number
  total_stock_units: number
  total_stock_value: number
  low_stock_products_count: number
  stock_by_category: StockByCategory[]
  movements_last_30_days: MovementData[]
  total_inbound_30_days: number
  total_outbound_30_days: number
  top_products_by_stock: TopProduct[]
  low_stock_alerts: LowStockAlert[]
  warehouse_utilization: WarehouseUtilization
  generated_at: string
}