import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Handles deprication warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    
    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/add/<string:name>')
def add(name):
    u = User(name = name)
    print("creating user", u)
    db.session.add(u)
    db.session.commit()
    return "user {} created".format(name)

@app.route('/delete/<string:name>')
def delete(name):
    u = User.query.filter_by(name=name).first_or_404()
    db.session.delete(u)
    db.session.commit()
    return "user deleted"

@app.route('/view')
def view():
   return User.query.all()
