from .extensions import db


def seed():
    # ==========================================================
    # MEMBER 1 — Seed sample users (admin + members)
    # ==========================================================

    # ==========================================================
    # MEMBER 2 — Seed sample authors, categories, books
    # ==========================================================

    # ==========================================================
    # MEMBER 3 — Seed sample borrow records
    # ==========================================================

    db.session.commit()
    print("Database seeded.")


if __name__ == "__main__":
    seed()
