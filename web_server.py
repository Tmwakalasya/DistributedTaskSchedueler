from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Tasks(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    parameters = db.Column(db.String(255))
    status = db.Column(db.String(20))
    timestamps = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    with app.app_context():
        db.create_all()

