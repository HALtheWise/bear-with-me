#!/usr/bin/env python3
import datetime
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
        set_user_active(msg.number, False)

        msg.text = SIGNDOWN_RESPONSE
        msg.send()
        return True

    if msg.text.upper() in SIGNUP_REQUESTS:
        set_user_active(msg.number, True)

        msg.text = SIGNUP_RESPONSE
        msg.send()
        return True

    msg.text = INSTRUCTIONS_RESPONSE
    msg.send()
    return False


def set_user_active(number, active=True, is_call=False):
    u = User.query.filter_by(phone=number).first()

    if u is None:
        # No user yet exists in the database with that phone number
        u = User(id=random.randint(0, 2**31), phone=number)

    u.active = active
    if is_call:
        u.last_call = datetime.datetime.now()
    print("creating user", u)
    db.session.add(u)
    db.session.commit()


def test():
    handle_message(next(get_old_messages()))

    return str(User.query.all())
