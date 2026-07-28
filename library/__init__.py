from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, bcrypt, login_manager, ma


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)

    # Register routes
    from .routes import auth_bp, users_bp, books_bp, authors_bp, categories_bp, borrow_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(borrow_bp)

    return app
