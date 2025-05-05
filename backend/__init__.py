from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")  # adjust if your config is elsewhere
    db.init_app(app)
    login_manager.init_app(app)

    from .models import User

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import views as views_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(views_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

