from .extensions import ma
from .models import User, BorrowRecord
from marshmallow import fields, validate, validates, ValidationError


# =============================================================
# MASON — Authentication & Users
# =============================================================

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        dump_only = ("id", "username", "email", "role", "created_at")

    password = fields.String(load_only=True)


class RegisterSchema(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8), load_only=True)
    password_confirmation = fields.String(required=True, load_only=True)

    @validates("username")
    def validate_username_unique(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError("Username already taken.")

    @validates("email")
    def validate_email_unique(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError("Email already registered.")

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        data = super().load(data, **kwargs)
        if data.get("password") != data.get("password_confirmation"):
            raise ValidationError({"password_confirmation": ["Passwords do not match."]})
        return data


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


# =============================================================
# NAOMI — Library Management
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
# NASRA — Borrowing System
# =============================================================
class BorrowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BorrowRecord
        dump_only = ("id", "borrow_date", "status")

    user = fields.Nested(UserSchema, dump_only=True)
    book = fields.Nested("BookSchema", dump_only=True)
