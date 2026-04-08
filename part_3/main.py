from flask import Flask, jsonify
from datetime import datetime, timedelta
from models import db, Company, Warehouse, Product, Inventory, Supplier, SupplierProduct, InventoryHistory
"""Assumption: SQLAlchemy ORM models exist for Company, Warehouse,
Product, Inventory, Supplier, SupplierProduct, and InventoryHistory.
These correspond to the database schema defined in Part 2."""

app = Flask(__name__)


@app.route("/api/companies/<int:company_id>/alerts/low-stock", methods=["GET"])
def low_stock_alerts(company_id):

    alerts = []

    # Step 1: Get warehouses belonging to the company
    warehouses = Warehouse.query.filter_by(company_id=company_id).all()

    if not warehouses:
        return {"alerts": [], "total_alerts": 0}

    warehouse_ids = [w.id for w in warehouses]

    # Step 2: Get inventory for these warehouses
    inventories = Inventory.query.filter(
        Inventory.warehouse_id.in_(warehouse_ids)
    ).all()

    for inv in inventories:

        product = Product.query.get(inv.product_id)

        # Step 3: Get product threshold from product type
        threshold = product.product_type.low_stock_threshold

        # Skip if stock is above threshold
        if inv.quantity >= threshold:
            continue

        # Step 4: Check recent sales activity (last 30 days)
        recent_sales = InventoryHistory.query.filter(
            InventoryHistory.product_id == product.id,
            InventoryHistory.change_type == "sale",
            InventoryHistory.changed_at >= datetime.utcnow() - timedelta(days=30)
        ).first()

        if not recent_sales:
            continue

        # Step 5: Fetch supplier information
        supplier_link = SupplierProduct.query.filter_by(product_id=product.id).first()

        supplier = None
        if supplier_link:
            supplier_data = Supplier.query.get(supplier_link.supplier_id)

            supplier = {
                "id": supplier_data.id,
                "name": supplier_data.name,
                "contact_email": supplier_data.contact_email
            }

        # Step 6: Estimate days until stockout
        # (simple assumption based on last 30 days sales)
        monthly_sales = InventoryHistory.query.filter(
            InventoryHistory.product_id == product.id,
            InventoryHistory.change_type == "sale",
            InventoryHistory.changed_at >= datetime.utcnow() - timedelta(days=30)
        ).count()

        daily_sales_rate = monthly_sales / 30 if monthly_sales else 0
        days_until_stockout = int(inv.quantity / daily_sales_rate) if daily_sales_rate else None

        warehouse = Warehouse.query.get(inv.warehouse_id)

        alerts.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "current_stock": inv.quantity,
            "threshold": threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": supplier
        })

    return {
        "alerts": alerts,
        "total_alerts": len(alerts)
    }