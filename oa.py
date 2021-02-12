from flask_oauthlib.client import OAuth
from decouple import config

oauth = OAuth()

github = oauth.remote_app(
    'github', 
    access_token_method="POST", 
    access_token_url= "https://github.com/login/oauth/access_token", 
    authorize_url="https://github.com/login/oauth/authorize", 
    base_url="https://api.github.com/", 
    consumer_key= config('GITHUB_CONSUMER_KEY'), 
    consumer_secret= config('GITHUB_CONSUMER_SECRET'), 
    request_token_params={"scope": "user:email"}, 
    request_token_url= None,
)

google = oauth.remote_app(
    'google', 
    access_token_method="POST", 
    access_token_url= "https://accounts.google.com/o/oauth2/token", 
    authorize_url="https://accounts.google.com/o/oauth2/auth", 
    base_url="https://www.googleapis.com/oauth2/v1/", 
    consumer_key= config('GOOGLE_CLIENT_ID'), 
    consumer_secret= config('GOOGLE_CLIENT_SECRET'), 
    request_token_params={"scope": ['openid', 'email', 'profile', 'https://www.googleapis.com/auth/calendar']}, 
    request_token_url= None,
)

def initialize_oauth(app):
    oauth.init_app(app)

