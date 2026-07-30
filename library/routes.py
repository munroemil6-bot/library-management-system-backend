from flask import request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from marshmallow import ValidationError
from . import app
from .extensions import db, bcrypt
from .models import User,  Book, BorrowRecord, Author, Category
from .schemas import UserSchema, RegisterSchema, LoginSchema, BorrowSchema, AuthorSchema, CategorySchema, BookSchema
from datetime import datetime, timedelta

user_schema = UserSchema()
users_schema = UserSchema(many=True)
register_schema = RegisterSchema()
login_schema = LoginSchema()
borrow_schema = BorrowSchema()


# MASON — Authentication & Users
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


# NAOMI — Library Management
from flask import request, jsonify
from flask_login import login_required, current_user
from app import app, db
from app.models.author import Author
from app.models.category import Category
from app.models.book import Book
from app.schemas.catalog_schema import (
    author_schema, authors_schema,
    category_schema, categories_schema,
    book_schema, books_schema
)
def is_admin():
    return getattr(current_user, 'role', None) == 'admin'


# ==========================================
# 1. AUTHOR ROUTES
# ==========================================

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify(authors_schema.dump(authors)), 200

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id, description="Author not found")
    return jsonify(author_schema.dump(author)), 200

@app.route('/authors', methods=['POST'])
@login_required
def create_author():
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"message": "Author name is required"}), 400

    new_author = Author(name=data['name'], biography=data.get('biography', ''))
    db.session.add(new_author)
    db.session.commit()
    return jsonify(author_schema.dump(new_author)), 201

@app.route('/authors/<int:author_id>', methods=['PATCH'])
@login_required
def update_author(author_id):
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    author = Author.query.get_or_404(author_id, description="Author not found")
    data = request.get_json() or {}

    if 'name' in data:
        author.name = data['name']
    if 'biography' in data:
        author.biography = data['biography']

    db.session.commit()
    return jsonify(author_schema.dump(author)), 200

@app.route('/authors/<int:author_id>', methods=['DELETE'])
@login_required
def delete_author(author_id):
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    author = Author.query.get_or_404(author_id, description="Author not found")
    if author.books:
        return jsonify({"message": "Cannot delete author associated with existing books"}), 400

    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": f"Author '{author.name}' deleted successfully"}), 200


# ==========================================
# 2. CATEGORY ROUTES
# ==========================================

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id, description="Category not found")
    return jsonify(category_schema.dump(category)), 200

@app.route('/categories', methods=['POST'])
@login_required
def create_category():
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"message": "Category name is required"}), 400

    existing = Category.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({"message": "Category name already exists"}), 400

    new_category = Category(name=data['name'], description=data.get('description', ''))
    db.session.add(new_category)
    db.session.commit()
    return jsonify(category_schema.dump(new_category)), 201

@app.route('/categories/<int:category_id>', methods=['PATCH'])
@login_required
def update_category(category_id):
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    category = Category.query.get_or_404(category_id, description="Category not found")
    data = request.get_json() or {}

    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']

    db.session.commit()
    return jsonify(category_schema.dump(category)), 200

@app.route('/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    category = Category.query.get_or_404(category_id, description="Category not found")
    if category.books:
        return jsonify({"message": "Cannot delete category associated with existing books"}), 400

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": f"Category '{category.name}' deleted successfully"}), 200


# ==========================================
# 3. BOOK ROUTES (Includes Search & Filtering)
# ==========================================

@app.route('/books', methods=['GET'])
def get_books():
    query = Book.query

    search = request.args.get('search')
    author_id = request.args.get('author_id')
    category_id = request.args.get('category_id')

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))
    if author_id:
        query = query.filter_by(author_id=author_id)
    if category_id:
        query = query.filter_by(category_id=category_id)

    books = query.all()
    return jsonify(books_schema.dump(books)), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id, description="Book not found")
    return jsonify(book_schema.dump(book)), 200

@app.route('/books', methods=['POST'])
@login_required
def create_book():
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    data = request.get_json() or {}
    required_fields = ['title', 'isbn', 'author_id', 'category_id']

    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    total_copies = data.get('copies', 1)

    new_book = Book(
        title=data['title'],
        isbn=data['isbn'],
        description=data.get('description', ''),
        published_year=data.get('published_year'),
        copies=total_copies,
        available_copies=data.get('available_copies', total_copies),
        author_id=data['author_id'],
        category_id=data['category_id']
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify(book_schema.dump(new_book)), 201

@app.route('/books/<int:book_id>', methods=['PATCH'])
@login_required
def update_book(book_id):
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    book = Book.query.get_or_404(book_id, description="Book not found")
    data = request.get_json() or {}

    for key in ['title', 'isbn', 'description', 'published_year', 'copies', 'available_copies', 'author_id', 'category_id']:
        if key in data:
            setattr(book, key, data[key])

    db.session.commit()
    return jsonify(book_schema.dump(book)), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    if not is_admin():
        return jsonify({"message": "Admin privileges required"}), 403

    book = Book.query.get_or_404(book_id, description="Book not found")
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book '{book.title}' deleted successfully"}), 200





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
