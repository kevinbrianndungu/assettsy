# backend/views.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Item
from .extensions import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def dashboard():
    items = Item.query.all()
    return render_template('dashboard.html', items=items)

@views.route('/add-item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if not name or not quantity or not price:
            flash('All fields are required.', 'danger')
            return redirect(url_for('views.add_item'))

        new_item = Item(name=name, quantity=int(quantity), price=float(price))
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully.', 'success')
        return redirect(url_for('views.dashboard'))

    return render_template('add_item.html')

@views.route('/delete-item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted.', 'info')
    return redirect(url_for('views.dashboard'))

@views.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        item.name = request.form.get('name')
        item.quantity = int(request.form.get('quantity'))
        item.price = float(request.form.get('price'))
        db.session.commit()
        flash('Item updated successfully.', 'success')
        return redirect(url_for('views.dashboard'))

    return render_template('edit_item.html', item=item)

