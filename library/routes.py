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
