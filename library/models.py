from .extensions import db
from flask_login import UserMixin
from datetime import datetime


# MASON — Authentication & Users
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



# NAOMI — Library Management
class Author(db.Model):
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
    published_year = db.Column(db.Integer, nullable=True)
    copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    author = db.relationship("Author", back_populates="books")
    category = db.relationship("Category", back_populates="books")
    borrow_records = db.relationship("BorrowRecord", back_populates="book", lazy=True)

    def __repr__(self):
        return f"<Book {self.title}>"


# NASRA — Borrowing System
class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'

    id = db.Column(db.Integer, primary_key=True)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='borrowed', nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    user = db.relationship('User', back_populates='borrow_records')
    book = db.relationship('Book', back_populates='borrow_records')

    def __repr__(self):
        return f'<BorrowRecord {self.id} user={self.user_id} book={self.book_id} status={self.status}>'
