# I might rename this to app.py and import it into __init__.py, to make the file structure more self-explanatory.
import html
import os
from datetime import datetime

from flask import Flask, request
from flask_migrate import Migrate

from app.models import *
from app import text_ui, twilio_interface, calls

# see the note in env.template.
DEV = os.getenv('FLASK_ENV') != "production"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Handles deprecation warning
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/message_handler', methods=['POST', 'GET'])
def handle_message():
    message = twilio_interface.Message(number=request.form['From'], text=request.form['Body'])
    text_ui.handle_message(message)
    return ''


@app.route('/')
def hello_world():
    """A landing page with basic instructions."""
    return 'Welcome to bear-with-me! To start, call the bear at ' + str(os.environ["TWILIO_PHONE_NUMBER"]) + '.'

# This is a lot of code to include in the dev case. (Think: prod/dev parity.) If
# it's only needed for manual unit testing, then it would presumably move to
# setup functions or a model layer once you implemented automated testing.
# If you need it in the workflow, I guess you're stuck with it. A slightly
# different approach would be to remove the `if DEV` guard, and add a middleware
# decorator that disables the route in production. I think I prefer that because
# it's more declarative, although it is also more mechanism to go wrong.
if DEV:
    @app.route('/test/add/')
    def add():
        u = User(phone='202-762-1401', active=True, last_call=datetime.now())  # TODO: Reasonable test data
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

    @app.route('/call/test', methods=['POST', 'GET'])
    def answer_test():
        msg = twilio_interface.Message(request.form['From'], "you called?")
        msg.send()
        return twilio_interface.dial(['202-480-9268', '202-762-1401'])

    @app.route('/view')
    def view():
        records = []
        for u in User.query.all():
            records.append(html.escape(str(u)))
        return '<br>'.join(records)


@app.route('/call/incoming', methods=['POST', 'GET'])
def answer():
    return calls.handle_incoming(request.form['From'])


if DEV:
    app.add_url_rule('/test/textui', 'test_textui', text_ui.test)
    app.add_url_rule('/test/twilio', 'test_twilio', twilio_interface.test)
