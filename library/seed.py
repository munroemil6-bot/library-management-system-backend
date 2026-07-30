from .extensions import db
from datetime import datetime, timedelta
from .models import User, Book, BorrowRecord


def seed():
    # MASON — Seed sample users (admin + members)
    if not User.query.first():
        users = [
            User(
                username="admin",
                email="admin@bookbarn.com",
                password_hash=bcrypt.generate_password_hash("admin1234").decode("utf-8"),
                role="admin",
            ),
            User(
                username="alice",
                email="alice@bookbarn.com",
                password_hash=bcrypt.generate_password_hash("alice1234").decode("utf-8"),
                role="member",
            ),
            User(
                username="bob",
                email="bob@bookbarn.com",
                password_hash=bcrypt.generate_password_hash("bob12345").decode("utf-8"),
                role="member",
            ),
        ]
        db.session.add_all(users)

    # ==========================================================
    # NAOMI — Seed sample authors, categories, books
    # ==========================================================



    # NASRA — Seed sample borrow records
    user = User.query.filter_by(username="testuser").first()
    book = Book.query.filter_by(isbn="1234567890").first()

    if user and book:
        record = BorrowRecord(
            user_id=user.id,
            book_id=book.id,
            due_date=datetime.utcnow() + timedelta(days=14),
        )
        db.session.add(record)
        print("Seeded 1 borrow record.")
    else:
        print("Skipped borrow record seed — user or book not found yet.")

    db.session.commit()
    print("Database seeded.")


if __name__ == "__main__":
    seed()
