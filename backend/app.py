from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# User loader needs to be declared after User model import
from backend.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configurations
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize app with extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from backend.auth import auth as auth_blueprint
    from backend.views import views as views_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(views_blueprint)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

