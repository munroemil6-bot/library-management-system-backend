from .extensions import db
from flask_login import UserMixin
from datetime import datetime


# =============================================================
# MASON — Authentication & Users
# =============================================================

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")  # "admin" or "member"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    borrow_records = db.relationship("BorrowRecord", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


# =============================================================
# NAOMI — Library Management
# TODO: Create the Author model
# Fields: id, name, biography
# Relationships: Author → Books (one-to-many)
#
# TODO: Create the Category model
# Fields: id, name, description
# Relationships: Category → Books (one-to-many)
#
# TODO: Create the Book model
# Fields: id, title, isbn, description, published_year,
#         copies, available_copies, author_id, category_id
# Relationships: Book → BorrowRecords (one-to-many)
# =============================================================


# =============================================================
# NASRA — Borrowing System
# TODO: Create the BorrowRecord model
# Fields: id, borrow_date, due_date, return_date, status,
#         user_id, book_id
# Status values: "borrowed", "returned", "overdue"
# Relationships: BorrowRecord → User, BorrowRecord → Book
# =============================================================
