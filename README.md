# Git-logger
This web app has been developed using the popular Django framework and Bootstrap for the frontend.

### Basic Features of The App
    
* Login - Registered users can login using username and password
* Social Apps Login – Users can login using their GitHub
* User Profile - Once logged in, users can create and update additional information such as avatar and bio in the profile page
* Update Profile – Users can update their information such as username, email, password, avatar and bio
* Remember me – Cookie Option, users don’t have to provide credentials every time they hit the site
* Forgot Password – Users can easily retrieve their password if they forget it 
* Admin Panel – admin can CRUD users

### Quick Start
To get this project up and running locally on your computer follow the following steps.
1. Set up a python virtual environment
2. Run the following commands
```
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
$ python3 manage.py runserver
```
   
3. Open a browser and go to http://localhost:8000/

