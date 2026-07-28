from .extensions import db
from flask_login import UserMixin
from datetime import datetime


# =============================================================
# MEMBER 1 — Authentication & Users
# TODO: Create the User model
# Fields: id, username, email, password_hash, role, created_at
# Relationships: User → BorrowRecord (one-to-many)
# Notes: role should support "admin" and "member"
# =============================================================


# =============================================================
# MEMBER 2 — Library Management
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
# MEMBER 3 — Borrowing System
# TODO: Create the BorrowRecord model
# Fields: id, borrow_date, due_date, return_date, status,
#         user_id, book_id
# Status values: "borrowed", "returned", "overdue"
# Relationships: BorrowRecord → User, BorrowRecord → Book
# =============================================================
