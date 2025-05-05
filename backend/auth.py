from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from backend.models import User
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # login logic here
    pass

