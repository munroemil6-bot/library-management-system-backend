from flask import request, jsonify
from flask_login import login_required, current_user
from . import app, db
from .models import BorrowRecord, Book
from .schemas import BorrowSchema
from datetime import datetime, timedelta

# =============================================================
# MASON — Authentication & Users
# =============================================================

# TODO: POST /register
# @app.route("/register", methods=["POST"])
# def register():
#     pass

# TODO: POST /login
# @app.route("/login", methods=["POST"])
# def login():
#     pass

# TODO: POST /logout
# @app.route("/logout", methods=["POST"])
# @login_required
# def logout():
#     pass

# TODO: GET /users
# @app.route("/users", methods=["GET"])
# @login_required
# def get_users():
#     pass

# TODO: GET /users/<id>
# @app.route("/users/<int:id>", methods=["GET"])
# @login_required
# def get_user(id):
#     pass

# TODO: PATCH /users/<id>
# @app.route("/users/<int:id>", methods=["PATCH"])
# @login_required
# def update_user(id):
#     pass

# TODO: DELETE /users/<id>
# @app.route("/users/<int:id>", methods=["DELETE"])
# @login_required
# def delete_user(id):
#     pass


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


# =============================================================
# NASRA — Borrowing System
# =============================================================
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
