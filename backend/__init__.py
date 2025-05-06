# backend/__init__.py

from flask import Flask
from .extensions import db, login_manager, migrate
from .views import views
from .auth import auth
from .models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Blueprint registration
    app.register_blueprint(views)
    app.register_blueprint(auth)

    # User loader for login_manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

