from flask import Flask
from .extensions import db, login_manager, migrate
from .views import views
from .auth import auth
from .models import User

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_mapping(
        SECRET_KEY='dev-key',  # Change to os.environ.get("SECRET_KEY") in production
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register user loader
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception as e:
            print(f"[LOGIN_MANAGER] Error loading user: {e}")
            return None

    # Register blueprints
    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app

