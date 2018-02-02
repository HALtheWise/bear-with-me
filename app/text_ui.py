#!/usr/bin/env python3
import datetime
import random

from app.models import db, User
from app.twilio_interface import Message, get_old_messages

SIGNUP_REQUESTS = ["I'm in", "call me"]
SIGNDOWN_REQUESTS = ["stop", "cancel"]

SIGNUP_REQUESTS = [s.upper() for s in SIGNUP_REQUESTS]
SIGNDOWN_REQUESTS = [s.upper() for s in SIGNDOWN_REQUESTS]


def handle_message(msg):
    """
    Takes action in response to a message including, if necessary, responding.
    :param (Message) msg: The incomming text message prompting the conversation
    :return: None
    """

    if msg.text.upper() in SIGNUP_REQUESTS:
        pass


def set_user_active(number, active=True, is_call=False):
    # q = User.query.filter_by(phone=number).first_or_404()

    if True:
        # TODO: check for existing user
        # No user exists in the database with that phone number
        u = User(id=random.randint(0, 2**31), phone=number, active=active)
        if is_call:
            u.last_call = datetime.datetime.now()
        print("creating user", u)
        db.session.add(u)
        db.session.commit()


def test():
    for msg in get_old_messages():
        set_user_active(msg.number)

    return 'Test Ran'


if __name__ == '__main__':
    test()
