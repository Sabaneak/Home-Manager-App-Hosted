# Home-Manager-App
Home-Manager is an API which can manage your day-to-day requirements, ranging from sending you reminders of your meetings to refill your pantry stock.  

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
> 3. Check username availability
> 4. Change Password
> 5. Token Refresh

> ### Card Categories
> Cards of these categories can be created, edited, deleted and viewed
> 1. Text
> 2. To-Do List
> 3. Meeting
> 4. Reminders
> 5. Refill

> ### Other Data Tables
> 1. Diary table
> 2. Stock table

## APIs Used
> 1. Sendgrid API: For sending instant/scheduled emails to user's email address
> 2. Twilio API: For sending SMS to registered phone numbers

## Softwares Used
1. Any text editor (Preferable VS Code or Pycharm)
2. Postman : For testing the endpoints. The collection is available in the repo in JSON form
3. Twilio and Sendgrid : For SMS and Email, as mentioned above
4. Python 3.8.3 (As of making this project)
5. Flask
6. MongoEngine (ORM for MongoDB) and MongoDB Compass (For monitoring database)


