from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict
from ..models import (
    Product, Inventory, Location, 
    InboundShipment, InboundShipmentItem,
    OutboundOrder, OutboundOrderItem
)
from ..schemas.dashboard import (
    DashboardSummary, StockByCategory, TopProduct,
    LowStockAlert, MovementData, WarehouseUtilization
)


class DashboardService:
    """Servicio para generar métricas y estadísticas del dashboard."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_summary(self) -> DashboardSummary:
        """
        Obtiene un resumen completo del dashboard con todas las métricas.
        
        Returns:
            DashboardSummary con todos los KPIs y análisis
        """
        return DashboardSummary(
            # KPIs principales
            total_products=self._get_total_products(),
            total_stock_units=self._get_total_stock_units(),
            total_stock_value=self._get_total_stock_value(),
            low_stock_products_count=self._get_low_stock_products_count(),
            
            # Stock por categoría
            stock_by_category=self._get_stock_by_category(),
            
            # Movimientos últimos 30 días
            movements_last_30_days=self._get_movements_last_30_days(),
            total_inbound_30_days=self._get_total_inbound_30_days(),
            total_outbound_30_days=self._get_total_outbound_30_days(),
            
            # Top productos
            top_products_by_stock=self._get_top_products_by_stock(),
            
            # Alertas
            low_stock_alerts=self._get_low_stock_alerts(),
            
            # Utilización del almacén
            warehouse_utilization=self._get_warehouse_utilization(),
            
            # Metadatos
            generated_at=datetime.utcnow()
        )
    
    def _get_total_products(self) -> int:
        """Cuenta el total de productos en el catálogo."""
        return self.db.query(Product).count()
    
    def _get_total_stock_units(self) -> int:
        """Suma todas las unidades en inventario."""
        result = self.db.query(func.sum(Inventory.quantity)).scalar()
        return int(result) if result else 0
    
    def _get_total_stock_value(self) -> float:
        """Calcula el valor total del inventario (cantidad * precio)."""
        result = self.db.query(
            func.sum(Inventory.quantity * Product.price)
        ).join(
            Product, Inventory.product_id == Product.id
        ).scalar()
        return float(result) if result else 0.0
    
    def _get_low_stock_products_count(self) -> int:
        """
        Cuenta productos que están por debajo de su nivel mínimo de stock.
        Agrupa por producto y compara el stock total vs min_stock_level.
        """
        subquery = self.db.query(
            Inventory.product_id,
            func.sum(Inventory.quantity).label('total_stock')
        ).group_by(Inventory.product_id).subquery()
        
        result = self.db.query(func.count()).select_from(Product).join(
            subquery, Product.id == subquery.c.product_id
        ).filter(
            subquery.c.total_stock < Product.min_stock_level
        ).scalar()
        
        return int(result) if result else 0
    
    def _get_stock_by_category(self) -> List[StockByCategory]:
        """
        Agrupa el stock por categoría de producto.
        
        Returns:
            Lista de StockByCategory con totales por categoría
        """
        results = self.db.query(
            Product.category,
            func.sum(Inventory.quantity).label('total_units'),
            func.sum(Inventory.quantity * Product.price).label('total_value')
        ).join(
            Inventory, Product.id == Inventory.product_id
        ).group_by(
            Product.category
        ).all()
        
        return [
            StockByCategory(
                category=row.category or "Sin categoría",
                total_units=int(row.total_units) if row.total_units else 0,
                total_value=float(row.total_value) if row.total_value else 0.0
            )
            for row in results
        ]
    
    def _get_movements_last_30_days(self) -> List[MovementData]:
        """
        Obtiene los movimientos de entrada y salida de los últimos 30 días.
        Agrupa por fecha para crear gráficos de línea.
        
        Returns:
            Lista de MovementData con inbound y outbound por día
        """
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Recepciones (inbound) - agrupadas por fecha de recepción
        inbound_data = self.db.query(
            func.date(InboundShipment.received_at).label('date'),
            func.sum(InboundShipmentItem.quantity_received).label('total')
        ).join(
            InboundShipmentItem, InboundShipment.id == InboundShipmentItem.shipment_id
        ).filter(
            InboundShipment.received_at >= thirty_days_ago,
            InboundShipment.received_at.isnot(None)
        ).group_by(
            func.date(InboundShipment.received_at)
        ).all()
        
        # Salidas (outbound) - agrupadas por fecha de envío
        outbound_data = self.db.query(
            func.date(OutboundOrder.shipped_at).label('date'),
            func.sum(OutboundOrderItem.quantity_picked).label('total')
        ).join(
            OutboundOrderItem, OutboundOrder.id == OutboundOrderItem.order_id
        ).filter(
            OutboundOrder.shipped_at >= thirty_days_ago,
            OutboundOrder.shipped_at.isnot(None)
        ).group_by(
            func.date(OutboundOrder.shipped_at)
        ).all()
        
        # Crear diccionario con todas las fechas de los últimos 30 días
        movements_dict: Dict[str, Dict[str, int]] = {}
        current_date = thirty_days_ago.date()
        end_date = datetime.utcnow().date()
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            movements_dict[date_str] = {'inbound': 0, 'outbound': 0}
            current_date += timedelta(days=1)
        
        # Llenar con datos de inbound
        for row in inbound_data:
            if row.date:
                date_str = row.date.strftime('%Y-%m-%d')
                if date_str in movements_dict:
                    movements_dict[date_str]['inbound'] = int(row.total) if row.total else 0
        
        # Llenar con datos de outbound
        for row in outbound_data:
            if row.date:
                date_str = row.date.strftime('%Y-%m-%d')
                if date_str in movements_dict:
                    movements_dict[date_str]['outbound'] = int(row.total) if row.total else 0
        
        # Convertir a lista ordenada
        return [
            MovementData(
                date=date_str,
                inbound=data['inbound'],
                outbound=data['outbound']
            )
            for date_str, data in sorted(movements_dict.items())
        ]
    
    def _get_total_inbound_30_days(self) -> int:
        """Suma total de unidades recibidas en los últimos 30 días."""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        result = self.db.query(
            func.sum(InboundShipmentItem.quantity_received)
        ).join(
            InboundShipment, InboundShipmentItem.shipment_id == InboundShipment.id
        ).filter(
            InboundShipment.received_at >= thirty_days_ago,
            InboundShipment.received_at.isnot(None)
        ).scalar()
        
        return int(result) if result else 0
    
    def _get_total_outbound_30_days(self) -> int:
        """Suma total de unidades enviadas en los últimos 30 días."""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        result = self.db.query(
            func.sum(OutboundOrderItem.quantity_picked)
        ).join(
            OutboundOrder, OutboundOrderItem.order_id == OutboundOrder.id
        ).filter(
            OutboundOrder.shipped_at >= thirty_days_ago,
            OutboundOrder.shipped_at.isnot(None)
        ).scalar()
        
        return int(result) if result else 0
    
    def _get_top_products_by_stock(self, limit: int = 5) -> List[TopProduct]:
        """
        Obtiene los productos con más stock en el almacén.
        
        Args:
            limit: Número de productos a retornar (default 5)
            
        Returns:
            Lista de TopProduct ordenados por stock descendente
        """
        results = self.db.query(
            Product.id,
            Product.sku,
            Product.name,
            func.sum(Inventory.quantity).label('total_stock'),
            func.sum(Inventory.quantity * Product.price).label('total_value')
        ).join(
            Inventory, Product.id == Inventory.product_id
        ).group_by(
            Product.id, Product.sku, Product.name
        ).order_by(
            desc('total_stock')
        ).limit(limit).all()
        
        return [
            TopProduct(
                product_id=row.id,
                sku=row.sku,
                name=row.name,
                total_stock=int(row.total_stock) if row.total_stock else 0,
                total_value=float(row.total_value) if row.total_value else 0.0
            )
            for row in results
        ]
    
    def _get_low_stock_alerts(self) -> List[LowStockAlert]:
        """
        Obtiene la lista de productos con stock por debajo del nivel mínimo.
        
        Returns:
            Lista de LowStockAlert con productos que necesitan reposición
        """
        subquery = self.db.query(
            Inventory.product_id,
            func.sum(Inventory.quantity).label('total_stock')
        ).group_by(Inventory.product_id).subquery()
        
        results = self.db.query(
            Product.id,
            Product.sku,
            Product.name,
            subquery.c.total_stock,
            Product.min_stock_level
        ).join(
            subquery, Product.id == subquery.c.product_id
        ).filter(
            subquery.c.total_stock < Product.min_stock_level
        ).order_by(
            (Product.min_stock_level - subquery.c.total_stock).desc()
        ).all()
        
        return [
            LowStockAlert(
                product_id=row.id,
                sku=row.sku,
                name=row.name,
                current_stock=int(row.total_stock) if row.total_stock else 0,
                min_stock_level=row.min_stock_level,
                difference=row.min_stock_level - (int(row.total_stock) if row.total_stock else 0)
            )
            for row in results
        ]
    
    def _get_warehouse_utilization(self) -> WarehouseUtilization:
        """
        Calcula la utilización del almacén (capacidad ocupada vs total).
        
        Returns:
            WarehouseUtilization con capacidad y porcentaje de uso
        """
        # Capacidad total de todas las ubicaciones
        total_capacity = self.db.query(
            func.sum(Location.capacity)
        ).scalar()
        total_capacity = int(total_capacity) if total_capacity else 0
        
        # Unidades ocupadas (total de stock)
        occupied_units = self._get_total_stock_units()
        
        # Calcular porcentaje
        utilization_percentage = 0.0
        if total_capacity > 0:
            utilization_percentage = (occupied_units / total_capacity) * 100
        
        available_capacity = total_capacity - occupied_units
        
        return WarehouseUtilization(
            total_capacity=total_capacity,
            occupied_units=occupied_units,
            utilization_percentage=round(utilization_percentage, 2),
            available_capacity=max(0, available_capacity)
        )


# Funciones helper para usar en las rutas
def get_dashboard_summary(db: Session) -> DashboardSummary:
    """
    Helper function para obtener el resumen del dashboard.
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        DashboardSummary con todas las métricas
    """
    service = DashboardService(db)
    return service.get_summary()

