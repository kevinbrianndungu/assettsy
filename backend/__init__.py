# backend/__init__.py

from flask import Flask
from .extensions import db, login_manager, migrate
from .views import views
from .auth import auth
from .models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # replace with a secure key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # User loader must be defined after app and db are initialized
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app

