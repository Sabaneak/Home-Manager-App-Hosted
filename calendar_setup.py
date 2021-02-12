from googleapiclient.discovery import build
import httplib2
from oauth2client import file, client, GOOGLE_TOKEN_URI

def create_service(access_token):
    """
    Function to create Google API client to access Calendar
    Input: Google Client Access Token
    Output: Google Calendar Build Object
    """
    credentials = client.AccessTokenCredentials(
        access_token,
        'calendar',
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service