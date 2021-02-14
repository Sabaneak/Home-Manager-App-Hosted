from .cards import Input_Cards, Cards, CardsList, CategoryList
from .diary import Diary_Entry, Diary, DiaryList
from .stock import Stock_Entry, Stock, StockList, Check_Refill
from .users import (
    UserRegister, 
    UserLogin,
    UserLogout, 
    TokenRefresh, 
    EmailConfirm,
    OTPConfirm,
    ChangePassword,
)
from .github_login import GithubLogin, GithubAuthorize
from .google_login import GoogleLogin, GoogleAuthorize
from .calendar import Calendar_SetUp, Create_Event, Get_Events, Delete_Events


def initialize_routes(api):
    """ Method to initialize all the routes """
    
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(TokenRefresh, '/refresh')
    
    api.add_resource(EmailConfirm, '/email_confirm/<string:_id>')
    api.add_resource(OTPConfirm, '/otp_confirm/<string:otp>')
    api.add_resource(ChangePassword, '/change_password/<string:password>')

    api.add_resource(GithubLogin, '/login/github')
    api.add_resource(GithubAuthorize, '/login/github/authorized', endpoint="github.authorize")
    api.add_resource(GoogleLogin, '/login/google')
    api.add_resource(GoogleAuthorize, '/login/google/authorized', endpoint="google.authorize")

    api.add_resource(Input_Cards, '/cards')
    api.add_resource(Cards, '/cards/<string:_id>')
    api.add_resource(CardsList, '/cards/all')
    api.add_resource(CategoryList, '/category/<string:category>')
    
    api.add_resource(Diary_Entry, '/diary')
    api.add_resource(Diary, '/diary/<string:_id>')
    api.add_resource(DiaryList, '/diary/all')

    api.add_resource(Stock_Entry, '/stock')
    api.add_resource(Stock, '/stock/<string:item>')
    api.add_resource(StockList, '/stock/all')
    api.add_resource(Check_Refill, '/refill')

    api.add_resource(Calendar_SetUp, '/calendar/<string:access_token>')
    api.add_resource(Delete_Events, '/calendar/delete/<string:access_token>')
    api.add_resource(Create_Event, '/calendar/event/<string:access_token>')
    api.add_resource(Get_Events, '/calendar/all/<string:access_token>')
    
   
