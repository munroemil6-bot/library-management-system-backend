from .extensions import db


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

    db.session.commit()
    print("Database seeded.")


if __name__ == "__main__":
    seed()
