from .extensions import db
from datetime import datetime, timedelta
from .models import User, Book, BorrowRecord


def seed():
    # ==========================================================
    # MASON — Seed sample users (admin + members)
    # ==========================================================

    # ==========================================================
    # NAOMI — Seed sample authors, categories, books
    # ==========================================================

    # ==========================================================
    # NASRA — Seed sample borrow records
    # ==========================================================
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
