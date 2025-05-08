from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Item
from .extensions import db
from collections import defaultdict
import csv
from io import TextIOWrapper
from flask import request

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def dashboard():
    items = Item.query.all()

    # Aggregating department data (count of items per department)
    dept_data = defaultdict(int)
    for item in items:
        dept_data[item.department] += 1

    # Convert dept_data to a regular dict (JSON serializable)
    dept_data = dict(dept_data)

    return render_template('dashboard.html', items=items, dept_data=dept_data, condition_data={})

@views.route('/add-item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        department = request.form.get('department')  # Assuming department is passed in the form

        if not name or not quantity or not price or not department:
            flash('All fields are required.', 'danger')
            return redirect(url_for('views.add_item'))

        new_item = Item(name=name, quantity=int(quantity), price=float(price), department=department)
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
        item.department = request.form.get('department')  # Assuming department is passed in the form
        db.session.commit()
        flash('Item updated successfully.', 'success')
        return redirect(url_for('views.dashboard'))

    return render_template('edit_item.html', item=item)

@views.route('/import-csv', methods=['GET', 'POST'])
@login_required
def import_csv():
    if request.method == 'POST':
        file = request.files['file']
        if not file or not file.filename.endswith('.csv'):
            flash('Please upload a valid CSV file.', 'danger')
            return redirect(url_for('views.import_csv'))

        stream = TextIOWrapper(file.stream)
        csv_reader = csv.DictReader(stream)

        count = 0
        for row in csv_reader:
            try:
                name = row['name']
                quantity = int(row['quantity'])
                price = float(row['price'])
                department = row['department']

                item = Item(name=name, quantity=quantity, price=price, department=department)
                db.session.add(item)
                count += 1
            except Exception as e:
                flash(f"Error processing row: {row} -> {e}", 'warning')
                continue

        db.session.commit()
        flash(f'Successfully imported {count} items.', 'success')
        return redirect(url_for('views.dashboard'))

    return render_template('import_csv.html')
