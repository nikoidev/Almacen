from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .core.database import engine, Base
from .api.routes import (
    auth, users, roles, permissions, audit_logs, profile,
    products, suppliers, locations, inventory, shipments, orders, dashboard
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SGA Pro API",
    description="Sistema de Gestión de Almacenes - Complete Warehouse Management System with Inventory Control, Inbound/Outbound Operations, RBAC and Audit Log",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers - Core
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(roles.router, prefix="/api/roles", tags=["Roles"])
app.include_router(permissions.router, prefix="/api/permissions", tags=["Permissions"])
app.include_router(audit_logs.router, prefix="/api/audit-logs", tags=["Audit Logs"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])

# Include routers - SGA (Warehouse Management)
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(suppliers.router, prefix="/api/suppliers", tags=["Suppliers"])
app.include_router(locations.router, prefix="/api/locations", tags=["Locations"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(shipments.router, prefix="/api/shipments", tags=["Inbound Shipments"])
app.include_router(orders.router, prefix="/api/orders", tags=["Outbound Orders"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


@app.get("/")
def root():
    return {
        "message": "SGA Pro - Sistema de Gestión de Almacenes API",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "Inventory Management",
            "Product Catalog",
            "Inbound Shipments",
            "Outbound Orders",
            "Dashboard & Analytics",
            "RBAC & Audit Log"
        ]
    }
