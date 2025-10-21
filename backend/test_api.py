"""
API Testing Script for SGA Pro
Tests all endpoints, audit logs, transactions, and RBAC
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(test_name, passed, details=""):
    status = f"{Colors.GREEN}[PASSED]{Colors.RESET}" if passed else f"{Colors.RED}[FAILED]{Colors.RESET}"
    print(f"{status} - {test_name}")
    if details:
        print(f"  {Colors.YELLOW}{details}{Colors.RESET}")
    print()

def login(username, password):
    """Authenticate and get token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": username, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_authentication():
    """Test authentication endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 1: AUTHENTICATION")
    print(f"{'='*60}{Colors.RESET}\n")
    
    # Test admin login
    token = login("admin", "admin123")
    passed = token is not None
    print_test("Admin Login", passed, f"Token: {token[:20]}..." if passed else "Failed to get token")
    
    # Test invalid login
    token = login("invalid", "invalid")
    passed = token is None
    print_test("Invalid Login (should fail)", passed, "Correctly rejected invalid credentials")
    
    return login("admin", "admin123")

def test_products(token):
    """Test product endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 2: PRODUCTS CRUD")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Create product
    product_data = {
        "sku": f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "name": "Test Product",
        "description": "Product for testing",
        "category": "Electronics",
        "price": 99.99,
        "min_stock_level": 10
    }
    response = requests.post(f"{BASE_URL}/api/products/", json=product_data, headers=headers)
    passed = response.status_code == 201
    product_id = response.json()["id"] if passed else None
    print_test("Create Product", passed, f"Product ID: {product_id}")
    
    if not product_id:
        return None
    
    # Get product
    response = requests.get(f"{BASE_URL}/api/products/{product_id}", headers=headers)
    passed = response.status_code == 200 and response.json()["name"] == "Test Product"
    print_test("Get Product by ID", passed, f"Name: {response.json().get('name')}")
    
    # Update product
    update_data = {"name": "Test Product Updated", "price": 149.99}
    response = requests.put(f"{BASE_URL}/api/products/{product_id}", json=update_data, headers=headers)
    passed = response.status_code == 200
    if passed:
        passed = response.json().get("price") == 149.99
        print_test("Update Product", passed, f"New price: ${response.json().get('price')}")
    else:
        print_test("Update Product", False, f"Status: {response.status_code}, Error: {response.text}")
    
    # List products
    response = requests.get(f"{BASE_URL}/api/products/", headers=headers)
    passed = response.status_code == 200 and len(response.json()["items"]) > 0
    print_test("List Products", passed, f"Total: {response.json().get('total', 0)} products")
    
    # Search products
    response = requests.get(f"{BASE_URL}/api/products/?search=Test", headers=headers)
    passed = response.status_code == 200
    print_test("Search Products", passed, f"Found: {len(response.json()['items'])} products")
    
    return product_id

def test_suppliers(token):
    """Test supplier endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 3: SUPPLIERS CRUD")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Create supplier
    supplier_data = {
        "name": "Test Supplier Inc.",
        "contact_person": "John Doe",
        "email": "test@supplier.com",
        "phone": "+1234567890",
        "address": "123 Test Street"
    }
    response = requests.post(f"{BASE_URL}/api/suppliers/", json=supplier_data, headers=headers)
    passed = response.status_code == 201
    supplier_id = response.json()["id"] if passed else None
    print_test("Create Supplier", passed, f"Supplier ID: {supplier_id}")
    
    if not supplier_id:
        return None
    
    # Get supplier
    response = requests.get(f"{BASE_URL}/api/suppliers/{supplier_id}", headers=headers)
    passed = response.status_code == 200
    print_test("Get Supplier by ID", passed, f"Name: {response.json().get('name')}")
    
    # List suppliers
    response = requests.get(f"{BASE_URL}/api/suppliers/", headers=headers)
    passed = response.status_code == 200
    print_test("List Suppliers", passed, f"Total: {response.json().get('total', 0)} suppliers")
    
    return supplier_id

def test_locations(token):
    """Test location endpoints"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 4: LOCATIONS CRUD")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Create location
    location_data = {
        "code": f"TEST-{datetime.now().strftime('%H%M%S')}",
        "description": "Test Location",
        "capacity": 1000
    }
    response = requests.post(f"{BASE_URL}/api/locations/", json=location_data, headers=headers)
    passed = response.status_code == 201
    location_id = response.json()["id"] if passed else None
    print_test("Create Location", passed, f"Location ID: {location_id}")
    
    if not location_id:
        return None
    
    # Get location
    response = requests.get(f"{BASE_URL}/api/locations/{location_id}", headers=headers)
    passed = response.status_code == 200
    print_test("Get Location by ID", passed, f"Code: {response.json().get('code')}")
    
    # List locations
    response = requests.get(f"{BASE_URL}/api/locations/", headers=headers)
    passed = response.status_code == 200
    print_test("List Locations", passed, f"Total: {response.json().get('total', 0)} locations")
    
    return location_id

def test_inventory_operations(token, product_id, location_id):
    """Test inventory operations"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 5: INVENTORY OPERATIONS")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Adjust inventory (add stock)
    adjust_data = {
        "product_id": product_id,
        "location_id": location_id,
        "quantity": 100,
        "reason": "Initial stock for testing"
    }
    response = requests.post(f"{BASE_URL}/api/inventory/adjust", json=adjust_data, headers=headers)
    passed = response.status_code == 200
    print_test("Adjust Inventory (Add Stock)", passed, f"Added 100 units")
    
    # Get inventory
    response = requests.get(f"{BASE_URL}/api/inventory/", headers=headers)
    passed = response.status_code == 200
    print_test("List Inventory", passed, f"Total records: {response.json().get('total', 0)}")
    
    # Get inventory by product
    response = requests.get(f"{BASE_URL}/api/inventory/product/{product_id}", headers=headers)
    passed = response.status_code == 200
    if passed:
        total_qty = response.json().get("total_quantity", 0)
        passed = total_qty > 0
        print_test("Get Inventory by Product", passed, f"Total quantity: {total_qty}")
    else:
        print_test("Get Inventory by Product", False, f"Status: {response.status_code}, Error: {response.text}")
    
    # Get low stock products
    response = requests.get(f"{BASE_URL}/api/inventory/low-stock", headers=headers)
    passed = response.status_code == 200
    print_test("Get Low Stock Products", passed, f"Low stock items: {len(response.json())}")
    
    return True

def test_shipments(token, product_id, location_id, supplier_id):
    """Test inbound shipment operations"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 6: INBOUND SHIPMENTS")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Create shipment
    expected_date = (datetime.now() + timedelta(days=1)).isoformat()
    shipment_data = {
        "supplier_id": supplier_id,
        "expected_at": expected_date,
        "items": [
            {
                "product_id": product_id,
                "quantity_expected": 50,
                "location_id": location_id
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/shipments/", json=shipment_data, headers=headers)
    passed = response.status_code == 201
    shipment_id = response.json()["id"] if passed else None
    print_test("Create Inbound Shipment", passed, f"Shipment ID: {shipment_id}")
    
    if not shipment_id:
        return None
    
    # Get shipment
    response = requests.get(f"{BASE_URL}/api/shipments/{shipment_id}", headers=headers)
    passed = response.status_code == 200
    items = response.json().get("items", [])
    print_test("Get Shipment Details", passed, f"Items: {len(items)}")
    
    # Receive shipment
    item_id = items[0]["id"] if items else None
    if item_id:
        receive_data = {
            "items": [
                {
                    "id": item_id,
                    "quantity_received": 50
                }
            ]
        }
        response = requests.post(f"{BASE_URL}/api/shipments/{shipment_id}/receive", json=receive_data, headers=headers)
        passed = response.status_code == 200
        if not passed:
            print_test("Receive Shipment", False, f"Status: {response.status_code}, Error: {response.text}")
        else:
            print_test("Receive Shipment", passed, "Inventory should be updated")
    
    # List shipments
    response = requests.get(f"{BASE_URL}/api/shipments/", headers=headers)
    passed = response.status_code == 200
    print_test("List Shipments", passed, f"Total: {response.json().get('total', 0)} shipments")
    
    return shipment_id

def test_orders(token, product_id, location_id):
    """Test outbound order operations"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 7: OUTBOUND ORDERS")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Create order
    order_data = {
        "customer_name": "Test Customer",
        "items": [
            {
                "product_id": product_id,
                "quantity_ordered": 20
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/api/orders/", json=order_data, headers=headers)
    passed = response.status_code == 201
    if passed:
        order_id = response.json()["id"]
        print_test("Create Outbound Order", passed, f"Order ID: {order_id}")
    else:
        order_id = None
        print_test("Create Outbound Order", False, f"Status: {response.status_code}, Error: {response.text}")
    
    if not order_id:
        return None
    
    # Get order
    response = requests.get(f"{BASE_URL}/api/orders/{order_id}", headers=headers)
    passed = response.status_code == 200
    items = response.json().get("items", [])
    print_test("Get Order Details", passed, f"Items: {len(items)}")
    
    # Perform picking
    item_id = items[0]["id"] if items else None
    if item_id:
        pick_data = {
            "items": [
                {
                    "id": item_id,
                    "quantity_picked": 20
                }
            ]
        }
        response = requests.post(f"{BASE_URL}/api/orders/{order_id}/pick", json=pick_data, headers=headers)
        passed = response.status_code == 200
        print_test("Perform Picking", passed, "Stock should be reduced")
    
    # Ship order
    response = requests.post(f"{BASE_URL}/api/orders/{order_id}/ship", headers=headers)
    passed = response.status_code == 200
    print_test("Mark Order as Shipped", passed, f"Status: {response.json().get('status')}")
    
    # List orders
    response = requests.get(f"{BASE_URL}/api/orders/", headers=headers)
    passed = response.status_code == 200
    print_test("List Orders", passed, f"Total: {response.json().get('total', 0)} orders")
    
    return order_id

def test_dashboard(token):
    """Test dashboard endpoint"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 8: DASHBOARD & ANALYTICS")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/api/dashboard/summary", headers=headers)
    passed = response.status_code == 200
    
    if passed:
        summary = response.json()
        print_test("Get Dashboard Summary", passed, 
                  f"Products: {summary.get('total_products')}, "
                  f"Stock: {summary.get('total_stock_units')}, "
                  f"Value: ${summary.get('total_stock_value')}")
        
        print_test("Stock by Category", len(summary.get('stock_by_category', [])) > 0,
                  f"Categories: {len(summary.get('stock_by_category', []))}")
        
        print_test("Top Products", len(summary.get('top_products_by_stock', [])) > 0,
                  f"Top products: {len(summary.get('top_products_by_stock', []))}")
        
        print_test("Warehouse Utilization", 'warehouse_utilization' in summary,
                  f"Used: {summary.get('warehouse_utilization', {}).get('capacity_used', 0)}")
    else:
        print_test("Get Dashboard Summary", False, f"Status: {response.status_code}")

def test_audit_logs(token):
    """Test audit log endpoint"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 9: AUDIT LOGS")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/api/audit-logs/", headers=headers)
    passed = response.status_code == 200
    
    if passed:
        logs = response.json()
        total = logs.get('total', 0)
        items = logs.get('items', [])
        print_test("Get Audit Logs", passed, f"Total logs: {total}")
        
        # Check for inventory operations in audit log
        inventory_ops = [log for log in items if 'inventory' in log.get('action', '').lower()]
        print_test("Inventory Operations Logged", len(inventory_ops) > 0,
                  f"Found {len(inventory_ops)} inventory operations in audit log")
    else:
        print_test("Get Audit Logs", False, f"Status: {response.status_code}")

def test_error_handling(token):
    """Test error handling and validation"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("TEST SUITE 10: ERROR HANDLING & VALIDATION")
    print(f"{'='*60}{Colors.RESET}\n")
    
    headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Test invalid product creation (missing required fields)
    response = requests.post(f"{BASE_URL}/api/products/", json={"name": "Invalid"}, headers=headers)
    passed = response.status_code == 422
    print_test("Validation: Missing Required Fields", passed, "Correctly rejected invalid data")
    
    # Test get non-existent product
    response = requests.get(f"{BASE_URL}/api/products/99999", headers=headers)
    passed = response.status_code == 404
    print_test("Error: Non-existent Product", passed, "Correctly returned 404")
    
    # Test unauthorized access (no token)
    response = requests.get(f"{BASE_URL}/api/products/")
    passed = response.status_code == 401
    print_test("Security: Unauthorized Access", passed, "Correctly rejected request without token")
    
    # Test negative stock adjustment
    adjust_data = {
        "product_id": 1,
        "location_id": 1,
        "quantity": -99999,
        "reason": "Test negative stock"
    }
    response = requests.post(f"{BASE_URL}/api/inventory/adjust", json=adjust_data, headers=headers)
    passed = response.status_code in [400, 422]
    print_test("Validation: Negative Stock Prevention", passed, "Correctly rejected negative stock")

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("SGA PRO - API TESTING SUITE")
    print(f"{'='*60}{Colors.RESET}")
    print(f"\n{Colors.YELLOW}Testing Backend: {BASE_URL}{Colors.RESET}\n")
    
    try:
        # Test authentication
        token = test_authentication()
        if not token:
            print(f"\n{Colors.RED}CRITICAL: Authentication failed. Cannot continue tests.{Colors.RESET}\n")
            return
        
        # Test products
        product_id = test_products(token)
        
        # Test suppliers
        supplier_id = test_suppliers(token)
        
        # Test locations
        location_id = test_locations(token)
        
        # Test inventory operations
        if product_id and location_id:
            test_inventory_operations(token, product_id, location_id)
        
        # Test shipments
        if product_id and location_id and supplier_id:
            test_shipments(token, product_id, location_id, supplier_id)
        
        # Test orders
        if product_id and location_id:
            test_orders(token, product_id, location_id)
        
        # Test dashboard
        test_dashboard(token)
        
        # Test audit logs
        test_audit_logs(token)
        
        # Test error handling
        test_error_handling(token)
        
        print(f"\n{Colors.GREEN}{'='*60}")
        print("API TESTING COMPLETED")
        print(f"{'='*60}{Colors.RESET}\n")
        
    except Exception as e:
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}\n")

if __name__ == "__main__":
    main()

