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
from typing import List, Optional
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 1. Base Class definition
class Base(DeclarativeBase):
    pass

# 2. Author Model
class Author(Base):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text)

    books = db.relationship("Book", back_populates="author", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Author {self.name}>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    books = db.relationship("Book", back_populates="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    published_year = db.Column(db.Integer)
    copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    author = db.relationship("Author", back_populates="books")
    category = db.relationship("Category", back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"


# =============================================================
# NASRA — Borrowing System
# TODO: Create the BorrowRecord model
# Fields: id, borrow_date, due_date, return_date, status,
#         user_id, book_id
# Status values: "borrowed", "returned", "overdue"
# Relationships: BorrowRecord → User, BorrowRecord → Book
# =============================================================
