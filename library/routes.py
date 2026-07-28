from flask import Blueprint
from flask_login import login_required


# =============================================================
# MEMBER 1 — Authentication & Users
# Blueprint prefix: /auth and /users
# =============================================================

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
users_bp = Blueprint("users", __name__, url_prefix="/users")

# TODO: POST   /auth/register
# TODO: POST   /auth/login
# TODO: POST   /auth/logout
# TODO: GET    /users
# TODO: GET    /users/<int:id>
# TODO: PATCH  /users/<int:id>
# TODO: DELETE /users/<int:id>


# =============================================================
# MEMBER 2 — Library Management
# Blueprint prefix: /books, /authors, /categories
# =============================================================

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

# TODO: GET    /books
# TODO: GET    /books/<int:id>
# TODO: POST   /books           (admin only)
# TODO: PATCH  /books/<int:id>  (admin only)
# TODO: DELETE /books/<int:id>  (admin only)

# TODO: GET    /authors
# TODO: POST   /authors         (admin only)
# TODO: PATCH  /authors/<int:id>(admin only)
# TODO: DELETE /authors/<int:id>(admin only)

# TODO: GET    /categories
# TODO: POST   /categories         (admin only)
# TODO: PATCH  /categories/<int:id>(admin only)
# TODO: DELETE /categories/<int:id>(admin only)


# =============================================================
# MEMBER 3 — Borrowing System
# Blueprint prefix: /borrow
# =============================================================

borrow_bp = Blueprint("borrow", __name__, url_prefix="/borrow")

# TODO: GET    /borrow              (admin sees all, member sees own)
# TODO: POST   /borrow              (member borrows a book)
# TODO: PATCH  /borrow/<int:id>     (mark returned)
# TODO: DELETE /borrow/<int:id>     (admin only)
