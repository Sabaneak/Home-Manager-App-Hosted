# Home-Manager-Hosted-App
Home-Manager is an API which can manage your day-to-day requirements, ranging from sending you reminders of your meetings to refill your pantry stock.  
The API is available on https://home-manage.herokuapp.com
 >> To test, replace the URL part in Postman environment with the heroku URL

## How to run
1. Open cmd and enter git clone repo-name
2. Create .env file and use the parameters from .env.example to replace with your own private data
2. Run the following commands in terminal:
  >> pipenv install  
  >> pipenv shell  
  >> python app.py  
3. And, you're done!

## Features
> ### User Security
> 1. Secure User registration via Email and Phone OTP
> 2. Github OAuth
> 3. Google OAuth
> 4. Check username availability
> 5. Change Password
> 6. Token Refresh

> ### Card Categories
> Cards of these categories can be created, edited, deleted and viewed
> 1. Meeting
> 2. Reminders
> 3. Refill
> 4. Miscallaneous

>As the card types change based on category and the json body, these are the formats of the bodies while sending requests

1. Meeting:
>{
> "category": "Meeting",
>    "data": 
>        { "url": "meet.google.com",
>        "documents": "book",
>        "date_time": "2021-02-18T14:26:00+05:30"
>        }
>}

2. Reminders:
>{
>    "category": "Reminder",
>    "data": 
>        { 
>            "date_time": ["2021-02-18T14:26:00+05:30", "2021-02-18T14:26:00+05:30"]
>        }
>}

3. Refill:
>{
>    "category": "Refill",
>    "item": "Milk",
>    "count": 20,
>    "date_time": "2021-01-23 15:50:00"
>}

4. Miscallaneous category
>{
>    "category": "xyz",
>    "data": 
>        { 
>            "abc": "efg"
>        }
>}

> ### Other Data Tables
> 1. Diary table
> 2. Stock table

## APIs Used
> 1. Sendgrid API: For sending instant/scheduled emails to user's email address
> 2. Twilio API: For sending SMS to registered phone numbers
> 3. Google Calendar API: For viewing calendars, creating/deleting events

## Softwares Used
1. Any text editor (Preferable VS Code or Pycharm)
2. Postman : For testing the endpoints. The collection is available in the repo in JSON form
3. Twilio, Sendgrid and Google Calendar : For SMS, Email and Calendar, as mentioned above
4. Python 3.8.3 (As of making this project)
5. Flask
6. Postgresql via Flask-SqlAlchemy


