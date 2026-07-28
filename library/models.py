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



from typing import List, Optional
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 1. Base Class definition
class Base(DeclarativeBase):
    pass

# 2. Author Model
class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    biography: Mapped[Optional[str]] = mapped_column(Text)

    # One Author -> Many Books
    books: Mapped[List["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Author(id={self.id}, name='{self.name}')>"

# 3. Category Model
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # One Category -> Many Books
    books: Mapped[List["Book"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"

# 4. Book Model
class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    published_year: Mapped[Optional[int]] = mapped_column(Integer)
    copies: Mapped[int] = mapped_column(Integer, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, default=1)

    # Foreign Keys linking to Author and Category
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    # Relationships back to Author and Category
    author: Mapped["Author"] = relationship(back_populates="books")
    category: Mapped["Category"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title='{self.title}')>"

# =============================================================
# NASRA — Borrowing System
# TODO: Create the BorrowRecord model
# Fields: id, borrow_date, due_date, return_date, status,
#         user_id, book_id
# Status values: "borrowed", "returned", "overdue"
# Relationships: BorrowRecord → User, BorrowRecord → Book
# =============================================================
