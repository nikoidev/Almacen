from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime


class StockByCategory(BaseModel):
    """Stock agrupado por categoría de producto."""
    category: str
    total_units: int
    total_value: float


class TopProduct(BaseModel):
    """Producto top por stock."""
    product_id: int
    sku: str
    name: str
    total_stock: int
    total_value: float


class LowStockAlert(BaseModel):
    """Alerta de producto con bajo stock."""
    product_id: int
    sku: str
    name: str
    current_stock: int
    min_stock_level: int
    difference: int


class MovementData(BaseModel):
    """Datos de movimientos de inventario."""
    date: str
    inbound: int
    outbound: int


class WarehouseUtilization(BaseModel):
    """Utilización del almacén."""
    total_capacity: int
    occupied_units: int
    utilization_percentage: float
    available_capacity: int


class DashboardSummary(BaseModel):
    """Resumen completo del dashboard con todas las métricas."""
    
    # KPIs principales
    total_products: int
    total_stock_units: int
    total_stock_value: float
    low_stock_products_count: int
    
    # Stock por categoría
    stock_by_category: List[StockByCategory]
    
    # Movimientos (últimos 30 días)
    movements_last_30_days: List[MovementData]
    total_inbound_30_days: int
    total_outbound_30_days: int
    
    # Top productos
    top_products_by_stock: List[TopProduct]
    
    # Alertas de bajo stock
    low_stock_alerts: List[LowStockAlert]
    
    # Utilización del almacén
    warehouse_utilization: WarehouseUtilization
    
    # Metadatos
    generated_at: datetime
    
    class Config:
        from_attributes = True

