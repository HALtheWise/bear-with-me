#!/usr/bin/env python3
from datetime import datetime
import random

from app.models import db, User
from app.twilio_interface import Message, get_old_messages

SIGNUP_REQUESTS = ["I'm in", "call me"]
SIGNDOWN_REQUESTS = ["I'm out", "cancel"]

SIGNUP_REQUESTS = [s.upper() for s in SIGNUP_REQUESTS]
SIGNDOWN_REQUESTS = [s.upper() for s in SIGNDOWN_REQUESTS]

SIGNDOWN_RESPONSE = '🐻: Sad to see you go, text "I\'m in" at any time to join again'
SIGNUP_RESPONSE = '🐻: Welcome to the experiment! ' \
                  'Call the bear at any time during SLAC to connect with a random Oliner!'
INSTRUCTIONS_RESPONSE = '🐻: Sorry, I didn\'t understand that. ' \
                        'Text "I\'m in" at any time to join, or "I\'m out" to get out.'


def handle_message(msg):
    """
    Takes action in response to a message including, if necessary, responding.
    :param (Message) msg: The incomming text message prompting the conversation
    :return (bool): Whether any database action was taken
    """
    print('Handling message "{}"'.format(msg.text))

    if msg.text.upper() in SIGNDOWN_REQUESTS:
        update_user(msg.number, False)

        msg.text = SIGNDOWN_RESPONSE
        msg.send()
        return True

    if msg.text.upper() in SIGNUP_REQUESTS:
        update_user(msg.number, True)

        msg.text = SIGNUP_RESPONSE
        msg.send()
        return True

    msg.text = INSTRUCTIONS_RESPONSE
    msg.send()
    return False


def update_user(number, active=None, call_time=False):
    """

    :param number:
    :param (bool) active:
    :param (datetime | bool) call_time: If True,
    :return bool created: Whether a new user had to be created
    """
    created = False

    u = User.query.filter_by(phone=number).first()

    if u is None:
        # No user yet exists in the database with that phone number
        u = User(id=random.randint(0, 2 ** 31), phone=number, active=False)
        created = True

    if active is not None:
        u.active = active

    if call_time:
        if call_time is True:
            call_time = datetime.now()
        u.last_call = call_time

    print("creating user", u)
    db.session.add(u)
    db.session.commit()

    return created


def test():
    handle_message(next(get_old_messages()))

    return str(User.query.all())
