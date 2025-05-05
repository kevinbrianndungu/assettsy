from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    barcode = db.Column(db.String(100), unique=True)
    condition = db.Column(db.String(50))  # e.g., Good, Fair, Damaged
    department = db.Column(db.String(100))
    employee = db.Column(db.String(100))

