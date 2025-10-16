from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import get_current_user
from ...models import User
from ...schemas.dashboard import DashboardSummary
from ...services.dashboard_service import get_dashboard_summary

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene un resumen completo del dashboard con todas las métricas del almacén.
    
    **Métricas incluidas:**
    - KPIs principales (total productos, unidades, valor del inventario)
    - Stock por categoría
    - Movimientos de los últimos 30 días (entradas vs salidas)
    - Top 5 productos por stock
    - Alertas de bajo stock
    - Utilización del almacén (capacidad ocupada)
    
    **Requiere:**
    - Autenticación (usuario logueado)
    
    **Returns:**
    - DashboardSummary con todas las métricas calculadas
    """
    return get_dashboard_summary(db)

