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
# =============================================================
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
