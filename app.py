
# from flask import Flask, request, jsonify
# from flask import render_template


from flask import Flask, request, jsonify
from flask_cors import CORS 

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = "inventory-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://@localhost/InventoryDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
)

db = SQLAlchemy(app)
jwt = JWTManager(app)
# Product Model
class Product(db.Model):

    __tablename__ = "Products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    category = db.Column(db.String(100))

    quantity = db.Column(db.Integer)

    price = db.Column(db.Float)
# User Model
class User(db.Model):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )    

# Home Route
@app.route("/")
def home():
    return "Inventory API Running"

# Add Product API(POST API)
# POST API - Add Product

@app.route("/products", methods=["POST"])
@jwt_required()
def add_product():

    data = request.json

    # Validation

    if not data["name"]:

        return jsonify({
            "message": "Product name is required"
        }), 400

    if data["quantity"] < 0:

        return jsonify({
            "message": "Quantity cannot be negative"
        }), 400

    if data["price"] <= 0:

        return jsonify({
            "message": "Price must be greater than zero"
        }), 400

    product = Product(
        name=data["name"],
        category=data["category"],
        quantity=data["quantity"],
        price=data["price"]
    )

    db.session.add(product)

    db.session.commit()

    return jsonify({
        "message": "Product Added Successfully"
    })


@app.route("/products", methods=["GET"])
def get_products():


    products = Product.query.all()

    result = []

    for p in products:

        result.append({
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "quantity": p.quantity,
            "price": p.price
        })

    return jsonify(result)

# SEARCH Product API
@app.route("/products/search", methods=["GET"])
def search_product():

    name = request.args.get("name")

    products = Product.query.filter(
        Product.name.ilike(f"%{name}%")
    ).all()

    result = []

    for p in products:

        result.append({
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "quantity": p.quantity,
            "price": p.price
        })

    return jsonify(result)

# LOW STOCK API
@app.route("/low-stock", methods=["GET"])
def low_stock():

    products = Product.query.filter(
        Product.quantity < 9
    ).all()

    result = []

    for p in products:

        result.append({
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity
        })

    return jsonify(result)

# UPDATE Product API
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    product = Product.query.get(id)

    if not product:

        return jsonify({
            "message": "Product Not Found"
        }), 404

    data = request.json

    product.name = data["name"]
    product.category = data["category"]
    product.quantity = data["quantity"]
    product.price = data["price"]

    db.session.commit()

    return jsonify({
        "message": "Product Updated Successfully"
    })

# DELETE Product API
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    product = Product.query.get(id)

    if not product:

        return jsonify({
            "message": "Product Not Found"
        }), 404

    db.session.delete(product)

    db.session.commit()

    return jsonify({
        "message": "Product Deleted Successfully"
    })
# REGISTER API
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    # Check if user already exists
    existing_user = User.query.filter_by(
        username=data["username"]
    ).first()

    if existing_user:

        return jsonify({
            "message": "Username already exists"
        }), 400

    # Hash password
    hashed_password = generate_password_hash(
        data["password"]
    )

    # Create new user
    user = User(
        username=data["username"],
        password=hashed_password
    )

    db.session.add(user)

    db.session.commit()

    return jsonify({
        "message": "User Registered Successfully"
    })

# LOGIN API
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    # Find user
    user = User.query.filter_by(
        username=data["username"]
    ).first()

    # Check username
    if not user:

        return jsonify({
            "message": "User not found"
        }), 404

    # Verify password
    if not check_password_hash(
        user.password,
        data["password"]
    ):

        return jsonify({
            "message": "Invalid password"
        }), 401

    # Generate JWT token
    access_token = create_access_token(
        identity=user.username
    )

    return jsonify({
        "message": "Login Successful",
        "token": access_token
    })

with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)    

