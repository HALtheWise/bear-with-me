import datetime
import os
from io import StringIO

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say, Dial

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

assert ACCOUNT_SID, 'Error: the TWILIO_ACCOUNT_SID is not set'
assert AUTH_TOKEN, 'Error: the TWILIO_AUTH_TOKEN is not set'
assert PHONE_NUMBER, 'Error: the TWILIO_PHONE_NUMBER is not set'

# You can also write:
#   ACCOUNT_SID = os.environ['ACCOUNT_SID]
# to auomatically get an error, if you give up programatic control over the
# error message. This will also get an error even in optimized code, where
# `assert` is compiled out — this is probably what you want. However, your
# code raises an exception when the `ACCOUNT_SID` environment variable is
# set, but to the empty string; `os.environ[…]` doesn't.

client = Client(ACCOUNT_SID, AUTH_TOKEN)
number, = client.incoming_phone_numbers.list(phone_number=PHONE_NUMBER)
number.update(voice_url="http://htl-p1-bear.herokuapp.com/call/incoming")


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


def say(text):
    response = VoiceResponse()
    response.say(text, voice='woman', language='en')
    return str(response)


def dial(numbers, flavor=''):
    response = VoiceResponse()
    for num in numbers:
        dial = Dial()
        dial.number(num)
        response.append(dial)

    if flavor:
        response.say(flavor, voice='woman', language='en')

    return str(response)


def get_old_messages(since=datetime.datetime.now() - datetime.timedelta(hours=1)):
    messages = client.api.messages.list(to=PHONE_NUMBER, date_sent_after=since)
    # Generators are handy when the data set is large or producing it has side
    # effects, but they make for fragile code, if the caller is modified to
    # iterates over them twice (they'll be unexpectedly empty the second time).
    return (Message(msg.from_, msg.body) for msg in messages)


def test():
    result = StringIO()
    print("Retrieving messages sent in the last hour", file=result)
    for msg in get_old_messages():
        print(msg, file=result)

    return result.getvalue()


if __name__ == '__main__':
    print(test())
