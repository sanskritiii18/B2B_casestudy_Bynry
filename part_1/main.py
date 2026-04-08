from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.exc import IntegrityError
from functools import wraps

app = Flask(__name__)
db = SQLAlchemy(app)

# Rate Limiting Setup
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])


# Dummy Authentication Decorator (Example)
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_role = request.headers.get("Role")
        if user_role != "admin":
            return {"error": "Unauthorized"}, 403
        return func(*args, **kwargs)
    return wrapper


# Models (Simplified)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    quantity = db.Column(db.Integer)


# ---------------- SERVICE LAYER ---------------- #

class ProductService:

    @staticmethod
    def create_product(data):

        # 1. Validate Required Fields
        required_fields = ["name", "sku", "price", "warehouse_id"]

        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        # 2. Price Validation
        if data["price"] < 0:
            return {"error": "Price must be greater than or equal to 0"}, 400

        # 3. Quantity Validation
        if data.get("initial_quantity", 0) < 0:
            return {"error": "Initial quantity cannot be negative"}, 400

        # 4. Warehouse Validation
        warehouse = Warehouse.query.get(data["warehouse_id"])
        if not warehouse:
            return {"error": "Invalid warehouse_id"}, 404

        # 5. SKU Uniqueness Check
        existing_product = Product.query.filter_by(sku=data["sku"]).first()
        if existing_product:
            return {"error": "SKU already exists"}, 409

        try:
            # Create product
            product = Product(
                name=data["name"],
                sku=data["sku"],
                price=data["price"]
            )

            db.session.add(product)
            db.session.flush()   # Get product.id without committing

            # Create inventory
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data["warehouse_id"],
                quantity=data.get("initial_quantity", 0)
            )

            db.session.add(inventory)

            # Single Transaction Commit
            db.session.commit()

            return {
                "message": "Product created successfully",
                "product_id": product.id
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {"error": "Database integrity error"}, 409

        except Exception:
            db.session.rollback()
            return {"error": "Unexpected server error"}, 500


# ---------------- ROUTE LAYER ---------------- #

@app.route("/api/products", methods=["POST"])
@limiter.limit("20 per minute")  # Rate limiting
@admin_required                   # Authentication
def create_product():
    data = request.get_json()
    return ProductService.create_product(data)


if __name__ == "__main__":
    app.run(debug=True)