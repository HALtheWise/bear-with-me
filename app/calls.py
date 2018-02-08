import random

from app import twilio_interface
from app.models import *
from app.text_ui import update_user

ONBOARDING_MSG = '🐻: Thanks for calling! ' \
                 'Reply "I\'m in" if you are OK with getting called by the bear ' \
                 'at some time during SLAC tonight.'

CALL_RESPONSE = '🐻: Thanks for calling! ' \
                'Text "I\'m in" at any time to join the experiment, or "I\'m out" to get out.'

FLAVOR = [
    'Do you remember when you wanted the things you have today?',
    'What is your name? Where does it come from?',
    'What is your quest?',
    'What is your favorite color?'
]

def add_sample_numbers():
    update_user()

def handle_incoming(number):
    """
    Handles a call from the given phone number, connecting it to other random numbers in the database
    :param number:
    :return: Message data commanding Twilio to dial the appropriate numbers in sequence.
    """
    # Respond via text
    created = update_user(number, call_time=True)
    if created:
        msg = twilio_interface.Message(number, ONBOARDING_MSG)
    else:
        msg = twilio_interface.Message(number, CALL_RESPONSE)
    msg.send()

    # Call somebody
    recipients = get_recipient_list(number)
    for number in recipients:
        # TODO: Use callbacks to only update the call times of people who actually get called
        update_user(number, call_time=True)

    flavor = random.choice(FLAVOR)

    return twilio_interface.dial(recipients, flavor)


def get_recipient_list(number, num_results=2):
    """
    :param (int) num_results: How many results to return
    :param number: The calling number
    :return list[str] numbers: The numbers to have in the queue
    """
    result = []

    users = User.query.filter_by(active=True).filter(User.phone != number).order_by(User.last_call).all()
    print(users)

    users = iter(users)

    while len(result) < num_results:
        try:
            u = next(users)  # type: User
            if u.phone == number:
                continue
            result.append(u.phone)
        except StopIteration:
            break

    return result
