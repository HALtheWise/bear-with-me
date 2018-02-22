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
    :param (Message) msg: The incoming text message prompting the conversation
    :return (bool): Whether any database action was taken
    """
    print('Handling message "{}"'.format(msg.text))

    text = msg.text.upper().strip()

    # If you were to get to testing or grow this program, you'd discover that
    # this is easier to test if split into (at least) two functions: a pure
    # function that categorizes the text's message type (or "intent", in
    # the argot of many conversational APIs); one that uses this to perform
    # the side effects here.

    if text in SIGNDOWN_REQUESTS:
        # I'd go with an explicit keyword parameter here, to make the code
        # more self-explanatory.
        update_user(msg.number, active=False)

        msg.text = SIGNDOWN_RESPONSE
        msg.send()
        return True

    if text in SIGNUP_REQUESTS:
        update_user(msg.number, active=True)

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
    # The above docstring seems to be using the Sphinx syntax for documenting
    # JavaScript parameter types ("the js domain", in Sphinx terminology).
    #
    # I may be wrong, but I think that for this to work with tooling you will
    # need either:
    #
    # (1)
    #   :param active
    #   :type bool
    #
    # Or (2) to use the napoleon extension, and either the Numpy or Google
    # docstring conventions, both of which are more readable and expressive.
    #
    # Also, active has type Optional[bool] (however you choose to write that),
    # which is important here.

    created = False

    u = User.query.filter_by(phone=number).first()

    if u is None:
        # No user yet exists in the database with that phone number
        #
        # This works here, with a single-node server. And it probably works
        # in a clustered deployment, because it's probably not possible for
        # this to get twice within the window between the query and the
        # add.  In generaly, though, be careful of this pattern — you'll want
        # an "upsert". That's the standard term but it's not actually spelled
        # that way when speaking to SQL, and it's implemented differently in
        # different databases.
        u = User(id=random.randint(0, 2 ** 31), phone=number, active=False)
        # Is it important that the user id be random? Otherwise, let the
        # database create it. If it's marked as a primary key, then it will
        # get a series that's used to initialize it if no value is supplied.
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
