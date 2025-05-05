from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from backend.models import db, Asset

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def dashboard():
    assets = Asset.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', assets=assets)

@views.route('/add', methods=['GET', 'POST'])
@login_required
def add_asset():
    if request.method == 'POST':
        name = request.form.get('name')
        value = request.form.get('value')
        asset = Asset(name=name, value=value, user_id=current_user.id)
        db.session.add(asset)
        db.session.commit()
        return redirect(url_for('views.dashboard'))
    return render_template('add_asset.html')

