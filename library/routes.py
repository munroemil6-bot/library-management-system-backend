from flask import request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from marshmallow import ValidationError
from . import app
from .extensions import db, bcrypt
from .models import User
from .schemas import UserSchema, RegisterSchema, LoginSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
register_schema = RegisterSchema()
login_schema = LoginSchema()


# =============================================================
# MASON — Authentication & Users
# =============================================================

@app.route("/register", methods=["POST"])
def register():
    try:
        data = register_schema.validate(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 422
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201


@app.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 422
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid email or password."}), 401
    login_user(user)
    return jsonify(user_schema.dump(user)), 200


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully."}), 200


@app.route("/users", methods=["GET"])
@login_required
def get_users():
    if current_user.role != "admin":
        return jsonify({"error": "Admins only."}), 403
    return jsonify(users_schema.dump(User.query.all())), 200


@app.route("/users/<int:id>", methods=["GET"])
@login_required
def get_user(id):
    if current_user.role != "admin" and current_user.id != id:
        return jsonify({"error": "Unauthorized."}), 403
    user = db.get_or_404(User, id)
    return jsonify(user_schema.dump(user)), 200


@app.route("/users/<int:id>", methods=["PATCH"])
@login_required
def update_user(id):
    if current_user.role != "admin" and current_user.id != id:
        return jsonify({"error": "Unauthorized."}), 403
    user = db.get_or_404(User, id)
    data = request.get_json()
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    if "role" in data and current_user.role == "admin":
        user.role = data["role"]
    db.session.commit()
    return jsonify(user_schema.dump(user)), 200


@app.route("/users/<int:id>", methods=["DELETE"])
@login_required
def delete_user(id):
    if current_user.role != "admin":
        return jsonify({"error": "Admins only."}), 403
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted."}), 200


# =============================================================
# NAOMI — Library Management
# =============================================================

# TODO: GET /books
# @app.route("/books", methods=["GET"])
# def get_books():
#     pass

# TODO: GET /books/<id>
# @app.route("/books/<int:id>", methods=["GET"])
# def get_book(id):
#     pass

# TODO: POST /books  (admin only)
# @app.route("/books", methods=["POST"])
# @login_required
# def create_book():
#     pass

# TODO: PATCH /books/<id>  (admin only)
# @app.route("/books/<int:id>", methods=["PATCH"])
# @login_required
# def update_book(id):
#     pass

# TODO: DELETE /books/<id>  (admin only)
# @app.route("/books/<int:id>", methods=["DELETE"])
# @login_required
# def delete_book(id):
#     pass

# TODO: GET /authors
# @app.route("/authors", methods=["GET"])
# def get_authors():
#     pass

# TODO: POST /authors  (admin only)
# @app.route("/authors", methods=["POST"])
# @login_required
# def create_author():
#     pass

# TODO: PATCH /authors/<id>  (admin only)
# @app.route("/authors/<int:id>", methods=["PATCH"])
# @login_required
# def update_author(id):
#     pass

# TODO: DELETE /authors/<id>  (admin only)
# @app.route("/authors/<int:id>", methods=["DELETE"])
# @login_required
# def delete_author(id):
#     pass

# TODO: GET /categories
# @app.route("/categories", methods=["GET"])
# def get_categories():
#     pass

# TODO: POST /categories  (admin only)
# @app.route("/categories", methods=["POST"])
# @login_required
# def create_category():
#     pass

# TODO: PATCH /categories/<id>  (admin only)
# @app.route("/categories/<int:id>", methods=["PATCH"])
# @login_required
# def update_category(id):
#     pass

# TODO: DELETE /categories/<id>  (admin only)
# @app.route("/categories/<int:id>", methods=["DELETE"])
# @login_required
# def delete_category(id):
#     pass


# NASRA — Borrowing System
@app.route("/borrow", methods=["GET"])
@login_required
def get_borrow_records():
    if current_user.role == "admin":
        records = BorrowRecord.query.all()
    else:
        records = BorrowRecord.query.filter_by(user_id=current_user.id).all()

    schema = BorrowSchema(many=True)
    return jsonify(schema.dump(records)), 200


@app.route("/borrow", methods=["POST"])
@login_required
def borrow_book():
    data = request.get_json()
    book_id = data.get("book_id")

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found."}), 404

    if book.available_copies <= 0:
        return jsonify({"error": "No available copies of this book."}), 400

    existing = BorrowRecord.query.filter_by(
        user_id=current_user.id, book_id=book_id, status="borrowed"
    ).first()
    if existing:
        return jsonify({"error": "You already have this book borrowed."}), 400

    new_record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        due_date=datetime.utcnow() + timedelta(days=14),
    )

    book.available_copies -= 1

    db.session.add(new_record)
    db.session.commit()

    schema = BorrowSchema()
    return jsonify(schema.dump(new_record)), 201


@app.route("/borrow/<int:id>", methods=["PATCH"])
@login_required
def return_book(id):
    record = BorrowRecord.query.get(id)
    if not record:
        return jsonify({"error": "Borrow record not found."}), 404

    if record.user_id != current_user.id and current_user.role != "admin":
        return jsonify(
          {"error": "You are not authorized to update this record."}), 403

    if record.status == "returned":
        return jsonify({"error": "This book has already been returned."}), 400

    record.return_date = datetime.utcnow()
    record.status = "returned"
    record.book.available_copies += 1

    db.session.commit()

    schema = BorrowSchema()
    return jsonify(schema.dump(record)), 200


@app.route("/borrow/<int:id>", methods=["DELETE"])
@login_required
def delete_borrow_record(id):
    if current_user.role != "admin":
        return jsonify(
          {"error": "Only admins can delete borrow records."}), 403

    record = BorrowRecord.query.get(id)
    if not record:
        return jsonify({"error": "Borrow record not found."}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Borrow record deleted."}), 200
