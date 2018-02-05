import html
import os
from datetime import datetime

from flask import Flask, request
from flask_migrate import Migrate

from app.models import *
from app import text_ui, twilio_interface

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Handles deprecation warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/message_handler', methods=['POST'])
def handle_message():
    message = twilio_interface.Message(number=request.form['From'], text=request.form['Body'])
    text_ui.handle_message(message)
    return ''


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/test/add/')
def add():
    u = User(phone='911',active=True,last_call=datetime.now()) #TODO: Reasonable test data
    print("creating user", u)
    db.session.add(u)
    db.session.commit()
    return "user created"


@app.route('/test/delete/')
def delete():
    u = User.query.first_or_404()
    db.session.delete(u)
    db.session.commit()
    return "user deleted"

@app.route('/call/incoming')
def answer():
    #msg = twilio_interface.Message(request.form['From'], "you called?")
    #msg.send()
    
    return twilio_interface.say("hello")

@app.route('/view')
def view():
    records = []
    for u in User.query.all():
        records.append(html.escape(str(u)))
    return '<br>'.join(records)


app.add_url_rule('/test/textui', 'test_textui', text_ui.test)
app.add_url_rule('/test/twilio', 'test_twilio', twilio_interface.test)
