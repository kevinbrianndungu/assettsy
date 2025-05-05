from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(100), nullable=False)  # Ensure this field exists
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='assets')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def dashboard():
    assets = Asset.query.all()
    categories = Category.query.all()

    # Department-wise data
    dept_data = db.session.query(Category.name.label('department'), func.count(Asset.id).label('count')) \
        .join(Asset, Asset.category_id == Category.id) \
        .group_by(Category.name).all()

    # Condition-wise data
    condition_data = db.session.query(Asset.condition, func.count(Asset.id).label('count')) \
        .group_by(Asset.condition).all()

    # Format data for JSON serialization
    dept_data_json = [{'department': d.department, 'count': d.count} for d in dept_data]
    condition_data_json = [{'condition': c.condition, 'count': c.count} for c in condition_data]

    return render_template(
        'dashboard.html',
        assets=assets,
        categories=categories,
        dept_data=dept_data_json,
        condition_data=condition_data_json
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_category', methods=['POST'])
@login_required
def add_category():
    name = request.form['name']
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_asset', methods=['POST'])
@login_required
def add_asset():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    condition = request.form['condition']
    category_id = int(request.form['category_id'])
    new_asset = Asset(name=name, quantity=quantity, condition=condition, category_id=category_id)
    db.session.add(new_asset)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/update_asset/<int:id>', methods=['POST'])
@login_required
def update_asset(id):
    data = request.get_json()
    asset = Asset.query.get_or_404(id)
    asset.quantity = int(data['quantity'])
    db.session.commit()
    return jsonify({"success": True})

@app.route('/delete_asset/<int:id>', methods=['POST'])
@login_required
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({"success": True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



