from flask import request, jsonify
from flask_login import login_required, current_user
from . import app


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
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.author import Author
from app.schemas.catalog_schema import author_schema, authors_schema

# Blueprint Definition
catalog_bp = Blueprint('catalog', __name__, url_prefix='/api')

# Helper function to restrict write access to Admins
def admin_required():
    return getattr(current_user, 'role', None) == 'admin'


# ==========================================
# AUTHOR ROUTES
# ==========================================

# 1. GET ALL AUTHORS / GET SINGLE AUTHOR
@catalog_bp.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify(authors_schema.dump(authors)), 200


@catalog_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id, description="Author not found")
    return jsonify(author_schema.dump(author)), 200


# 2. CREATE AUTHOR (POST)
@catalog_bp.route('/authors', methods=['POST'])
@login_required
def create_author():
    if not admin_required():
        return jsonify({"message": "Admin privileges required"}), 403

    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"message": "Author name is required"}), 400

    new_author = Author(
        name=data['name'],
        biography=data.get('biography', '')
    )

    db.session.add(new_author)
    db.session.commit()

    return jsonify(author_schema.dump(new_author)), 201


# 3. UPDATE AUTHOR (PATCH)
@catalog_bp.route('/authors/<int:author_id>', methods=['PATCH'])
@login_required
def update_author(author_id):
    if not admin_required():
        return jsonify({"message": "Admin privileges required"}), 403

    author = Author.query.get_or_404(author_id, description="Author not found")
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    
    if 'name' in data:
        author.name = data['name']
    if 'biography' in data:
        author.biography = data['biography']

    db.session.commit()

    return jsonify(author_schema.dump(author)), 200


# 4. DELETE AUTHOR (DELETE)
@catalog_bp.route('/authors/<int:author_id>', methods=['DELETE'])
@login_required
def delete_author(author_id):
    if not admin_required():
        return jsonify({"message": "Admin privileges required"}), 403

    author = Author.query.get_or_404(author_id, description="Author not found")

    
    if author.books:
        return jsonify({"message": "Cannot delete author associated with existing books"}), 400

    db.session.delete(author)
    db.session.commit()

    return jsonify({"message": f"Author '{author.name}' deleted successfully"}), 200
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

# TODO: GET /borrow  (admin sees all, member sees own)
# @app.route("/borrow", methods=["GET"])
# @login_required
# def get_borrow_records():
#     pass

# TODO: POST /borrow  (member borrows a book)
# @app.route("/borrow", methods=["POST"])
# @login_required
# def borrow_book():
#     pass

# TODO: PATCH /borrow/<id>  (mark returned)
# @app.route("/borrow/<int:id>", methods=["PATCH"])
# @login_required
# def return_book(id):
#     pass

# TODO: DELETE /borrow/<id>  (admin only)
# @app.route("/borrow/<int:id>", methods=["DELETE"])
# @login_required
# def delete_borrow_record(id):
#     pass
