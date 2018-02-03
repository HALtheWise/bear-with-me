import datetime
import os
from io import StringIO

from twilio.rest import Client

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

assert ACCOUNT_SID, 'Error: the TWILIO_ACCOUNT_SID is not set'
assert AUTH_TOKEN, 'Error: the TWILIO_AUTH_TOKEN is not set'
assert PHONE_NUMBER, 'Error: the TWILIO_PHONE_NUMBER is not set'

client = Client(ACCOUNT_SID, AUTH_TOKEN)


class Message(object):
    """
    This is the internal representation of an incomming or outgoing text message.
    The number stored here is the phone number ('+15555555555') of the participant in the exchange
    that is not the bear.
    """

    def __init__(self, number, text):
        """
        :type number: str
        :type text: str
        """
        self.text = text
        self.number = number

    def __repr__(self):
        return '({}): "{}"'.format(self.number, self.text)

    def send(self):
        client.api.account.messages.create(
            to=self.number,
            from_=PHONE_NUMBER,
            body=self.text
        )


def get_old_messages(since=datetime.datetime.now() - datetime.timedelta(hours=1)):
    messages = client.api.messages.list(to=PHONE_NUMBER, date_sent_after=since)
    return (Message(msg.from_, msg.body) for msg in messages)


def test():
    result = StringIO()
    print("Retrieving messages sent in the last hour", file=result)
    for msg in get_old_messages():
        print(msg, file=result)

    return result.getvalue()


if __name__ == '__main__':
    print(test())
