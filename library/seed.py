from .extensions import db, bcrypt
from .models import User


def seed():
    # ==========================================================
    # MASON — Seed sample users (admin + members)
    # ==========================================================
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

    # ==========================================================
    # NASRA — Seed sample borrow records
    # ==========================================================

    db.session.commit()
    print("Database seeded.")


if __name__ == "__main__":
    seed()
