from twilio.rest import Client
from decouple import config

class Send_SMS: 
    """
    Library to send SMS via Twilio API.
    Env variables: Account ID, Auth Token
    """
    TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')

    @classmethod
    def send_sms(cls, content, receiver):
        """
        Method to send sms for registration.
        Params: -
            content: OTP randomly generated.
            receiver: Phone number user registers with.
        Output: SMS sent
        """
        client = Client(cls.TWILIO_ACCOUNT_SID, cls.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
                    body = content,
                    from_= config("PHONE_NUMBER"),
                    to= receiver,
        )
        return message