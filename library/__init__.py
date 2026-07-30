import os
from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, bcrypt, login_manager, ma

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.instance_path, exist_ok=True)

# Allow credentialed requests from local dev servers so the browser can receive
# and send the session cookie during cross-origin calls from Vite.
CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:5175",
            "http://localhost:5176",
            "http://localhost:5177",
            "http://localhost:5178",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:5175",
            "http://127.0.0.1:5176",
            "http://127.0.0.1:5177",
            "http://127.0.0.1:5178",
        ]
    }
})

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
ma.init_app(app)

from .models import User
from .seed import seed_if_empty

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from . import routes

with app.app_context():
    db.create_all()
    seed_if_empty()
