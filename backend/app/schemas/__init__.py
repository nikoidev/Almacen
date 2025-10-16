from .user import UserCreate, UserUpdate, UserResponse, UserLogin
from .role import RoleCreate, RoleUpdate, RoleResponse
from .permission import PermissionCreate, PermissionUpdate, PermissionResponse
from .token import Token, TokenData

# SGA Schemas
from .product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductListResponse, ProductInInventory
)
from .supplier import (
    SupplierCreate, SupplierUpdate, SupplierResponse,
    SupplierListResponse, SupplierInShipment
)
from .location import (
    LocationCreate, LocationUpdate, LocationResponse,
    LocationListResponse, LocationInInventory
)
from .inventory import (
    InventoryCreate, InventoryUpdate, InventoryResponse,
    InventoryListResponse, InventoryAdjust, InventoryMove,
    InventoryByProduct, LowStockProduct
)
from .shipment import (
    InboundShipmentCreate, InboundShipmentUpdate, InboundShipmentResponse,
    InboundShipmentListResponse, InboundShipmentReceive,
    InboundShipmentItemResponse
)
from .order import (
    OutboundOrderCreate, OutboundOrderUpdate, OutboundOrderResponse,
    OutboundOrderListResponse, OutboundOrderPick,
    OutboundOrderItemResponse
)

__all__ = [
    # Auth & Users
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin",
    "RoleCreate", "RoleUpdate", "RoleResponse",
    "PermissionCreate", "PermissionUpdate", "PermissionResponse",
    "Token", "TokenData",
    # Products
    "ProductCreate", "ProductUpdate", "ProductResponse",
    "ProductListResponse", "ProductInInventory",
    # Suppliers
    "SupplierCreate", "SupplierUpdate", "SupplierResponse",
    "SupplierListResponse", "SupplierInShipment",
    # Locations
    "LocationCreate", "LocationUpdate", "LocationResponse",
    "LocationListResponse", "LocationInInventory",
    # Inventory
    "InventoryCreate", "InventoryUpdate", "InventoryResponse",
    "InventoryListResponse", "InventoryAdjust", "InventoryMove",
    "InventoryByProduct", "LowStockProduct",
    # Shipments
    "InboundShipmentCreate", "InboundShipmentUpdate", "InboundShipmentResponse",
    "InboundShipmentListResponse", "InboundShipmentReceive",
    "InboundShipmentItemResponse",
    # Orders
    "OutboundOrderCreate", "OutboundOrderUpdate", "OutboundOrderResponse",
    "OutboundOrderListResponse", "OutboundOrderPick",
    "OutboundOrderItemResponse"
]
