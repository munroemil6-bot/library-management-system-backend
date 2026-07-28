from .extensions import ma
from marshmallow import fields, validate, validates, ValidationError


# =============================================================
# MEMBER 1 — Authentication & Users
# TODO: Create UserSchema
#   - Dump only: id, username, email, role, created_at
#   - Load only: password (write-only)
#
# TODO: Create RegisterSchema
#   - Validate: username (required, unique)
#   - Validate: email (required, valid format, unique)
#   - Validate: password (required, min 8 chars)
#   - Validate: password_confirmation (must match password)
#
# TODO: Create LoginSchema
#   - Fields: email, password
# =============================================================


# =============================================================
# MEMBER 2 — Library Management
# TODO: Create AuthorSchema
#   - Fields: id, name, biography
#   - Nested: books (many, dump only)
#
# TODO: Create CategorySchema
#   - Fields: id, name, description
#   - Nested: books (many, dump only)
#
# TODO: Create BookSchema
#   - Fields: id, title, isbn, description, published_year,
#             copies, available_copies, author_id, category_id
#   - Validate: copies >= 0, available_copies <= copies
#   - Validate: isbn unique
# =============================================================


# =============================================================
# MEMBER 3 — Borrowing System
# TODO: Create BorrowSchema
#   - Fields: id, borrow_date, due_date, return_date,
#             status, user_id, book_id
#   - Nested: user (dump only), book (dump only)
# =============================================================
