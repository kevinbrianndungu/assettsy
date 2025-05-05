from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with env variable in prod
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Import models (to register them with SQLAlchemy)
    from backend.models import User, Asset, Category

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Login manager setup
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from backend.views import views as views_blueprint
    from backend.auth import auth as auth_blueprint

    app.register_blueprint(views_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

