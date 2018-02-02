import os

from flask import Flask
from flask_migrate import Migrate

from app.models import *
from app import text_ui

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Handles deprecation warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/add/<string:name>')
def add(name):
    u = User(name=name)
    print("creating user", u)
    db.session.add(u)
    db.session.commit()
    return "user {} created".format(name)


app.add_url_rule('/test/textui', 'test_textui', text_ui.test)


@app.route('/delete/<string:name>')
def delete(name):
    u = User.query.filter_by(name=name).first_or_404()
    db.session.delete(u)
    db.session.commit()
    return "user deleted"


@app.route('/view')
def view():
    return User.query.all()
