# backend/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions (not tied to any app yet)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Optional: Configure login view
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

