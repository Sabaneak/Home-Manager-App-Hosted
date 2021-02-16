from twilio.rest import Client
from decouple import config

class Send_SMS: 
    """
    Library to send SMS via Twilio API.
    Env variables: Account ID, Auth Token
    """
    TWILIO_ACC_SID = config('TWILIO_ACC_SID')
    TWILIO_AUTH = config('TWILIO_AUTH')

    @classmethod
    def send_sms(cls, content, receiver):
        """
        Method to send sms for registration.
        Params: -
            content: OTP randomly generated.
            receiver: Phone number user registers with.
        Output: SMS sent
        """
        client = Client(cls.TWILIO_ACC_SID, cls.TWILIO_AUTH)
        message = client.messages.create(
                    body = content,
                    from_= config("PHONE_NUMBER"),
                    to= receiver,
        )
        return message