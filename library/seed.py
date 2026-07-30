from .extensions import db, bcrypt
from datetime import datetime, timedelta
from .models import User, Book, BorrowRecord, Author, Category
from . import app


def seed_if_empty():
    with app.app_context():
        if Book.query.count() > 0 or Author.query.count() > 0 or Category.query.count() > 0:
            return False
        seed()
        return True


def seed():
    # MASON — Seed sample users (admin + members)
    users_data = [
        {"username": "admin", "email": "admin@gmail.com", "password": "admin1234", "role": "admin"},
        {"username": "alice", "email": "alice@gmail.com", "password": "alice1234", "role": "member"},
        {"username": "bob", "email": "bob@gmail.com", "password": "bob12345", "role": "member"},
    ]

    for u in users_data:
        existing = User.query.filter_by(email=u["email"]).first()
        if not existing:
            new_user = User(
                username=u["username"],
                email=u["email"],
                password_hash=bcrypt.generate_password_hash(u["password"]).decode("utf-8"),
                role=u["role"],
            )
            db.session.add(new_user)

    # NAOMI — Seed sample authors and categories
    authors = [
        {"name": "George Orwell", "biography": "English novelist, essayist and critic."},
        {"name": "Jane Austen", "biography": "English novelist known primarily for her six major novels."},
        {"name": "Harper Lee", "biography": "American novelist widely known for To Kill a Mockingbird."},
        {"name": "J.K. Rowling", "biography": "British author, best known for the Harry Potter series."},
    ]

    for a in authors:
        if not Author.query.filter_by(name=a["name"]).first():
            db.session.add(Author(name=a["name"], biography=a.get("biography", "")))

    categories = [
        {"name": "Fiction", "description": "General fiction"},
        {"name": "Classics", "description": "Classic literature"},
        {"name": "Young Adult", "description": "YA and coming-of-age stories"},
        {"name": "Non-Fiction", "description": "Informative and factual books"},
    ]

    for c in categories:
        if not Category.query.filter_by(name=c["name"]).first():
            db.session.add(Category(name=c["name"], description=c.get("description", "")))

    db.session.commit()  # commit authors/categories so we can reference them

    # NAOMI — Seed sample books
    sample_books = [
        {
            "title": "1984",
            "isbn": "9780451524935",
            "description": "Dystopian novel by George Orwell.",
            "published_year": 1949,
            "copies": 3,
            "author_name": "George Orwell",
            "category_name": "Classics",
        },
        {
            "title": "Pride and Prejudice",
            "isbn": "9780141439518",
            "description": "A romantic novel by Jane Austen.",
            "published_year": 1813,
            "copies": 2,
            "author_name": "Jane Austen",
            "category_name": "Classics",
        },
        {
            "title": "To Kill a Mockingbird",
            "isbn": "9780060935467",
            "description": "Novel by Harper Lee.",
            "published_year": 1960,
            "copies": 4,
            "author_name": "Harper Lee",
            "category_name": "Fiction",
        },
        {
            "title": "Harry Potter and the Sorcerer's Stone",
            "isbn": "9780590353427",
            "description": "First book in the Harry Potter series.",
            "published_year": 1997,
            "copies": 5,
            "author_name": "J.K. Rowling",
            "category_name": "Young Adult",
        },
    ]

    for b in sample_books:
        if not Book.query.filter_by(isbn=b["isbn"]).first():
            author = Author.query.filter_by(name=b["author_name"]).first()
            category = Category.query.filter_by(name=b["category_name"]).first()
            if not author or not category:
                continue
            book = Book(
                title=b["title"],
                isbn=b["isbn"],
                description=b.get("description", ""),
                published_year=b.get("published_year"),
                copies=b.get("copies", 1),
                available_copies=b.get("copies", 1),
                author_id=author.id,
                category_id=category.id,
            )
            db.session.add(book)

    db.session.commit()

    # NASRA — Seed sample borrow records (make one sample borrow for alice)
    alice = User.query.filter_by(username="alice").first()
    sample_book = Book.query.filter_by(isbn="9780451524935").first()  # 1984
    if alice and sample_book:
        existing = BorrowRecord.query.filter_by(user_id=alice.id, book_id=sample_book.id, status="borrowed").first()
        if not existing and sample_book.available_copies > 0:
            record = BorrowRecord(
                user_id=alice.id,
                book_id=sample_book.id,
                due_date=datetime.utcnow() + timedelta(days=14),
            )
            sample_book.available_copies -= 1
            db.session.add(record)

    db.session.commit()
    print("Database seeded.")


if __name__ == "__main__":
    # Run under app context so models/db operate correctly
    with app.app_context():
        seed()
