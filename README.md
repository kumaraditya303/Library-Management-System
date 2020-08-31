![Build Status](https://travis-ci.org/kumaraditya303/Library-Management-System.svg?branch=master)

![Python package](https://github.com/kumaraditya303/Library-Management-System/workflows/Python%20package/badge.svg?branch=master) 

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fkumaraditya303%2FLibrary-Management-System&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

# Library Management System

A Python Flask based Library Management System. This Flask app has all the features of a Library Management System like adding, removing, and creating copies of books. A user can issue 2 books at ones. This app has a separate admin tab for admin users. This project also has mail functionality to send mails to user for notification.
Project live on [Heroku](http://librarymgmtsystem.herokuapp.com)
# Screenshot
<img src='https://github.com/rahuladitya303/Library-Managament-System/blob/master/Library_Management_System/static/screenshot.png'/>

___

# Project Structure

```sh
.
├── config.py  
├── data.db  
├── Library_Management_System  
│   ├── __init__.py  
│   ├── models.py  
│   ├── static  
│   │   ├── script.js  
│   │   └── user.png  
│   ├── templates  
│   │   ├── add_book.html  
│   │   ├── admin_dashboard.html  
│   │   ├── admin.html  
│   │   ├── admin_layout.html  
│   │   ├── dashboard.html  
│   │   ├── index.html  
│   │   ├── issue.html  
│   │   ├── login.html  
│   │   ├── register.html  
│   │   ├── remove_book.html  
│   │   ├── return.html  
│   │   ├── withlogin.html  
│   │   └── withoutlogin.html  
│   └── views.py  
├── LICENSE  
├── README.md  
├── requirements.txt  
├── runserver.py  
└── tests  
    ├── __init__.py  
    └── test_view.py  
```
___

# Configuration
- Make the changes to these lines in [config.py](https://github.com/rahuladitya303/Library-Managament-System/blob/master/config.py)
```python
    MAIL_SERVER = 'SMTP_SERVER'
    MAIL_PORT = 465 # SMTP PORT
    MAIL_USE_TLS = False # USE TTL
    MAIL_USE_SSL = True # USE SSL
    MAIL_USERNAME = '**********' # MAIL USERNAME
    MAIL_PASSWORD = '**********' # MAIL PASSWORD
    ADMIN_USERNAME = 'ADMIN_USERNAME' # ADMIN USERNAME
    ADMIN_PASSWORD = 'ADMIN_PASSWORD' # ADMIN PASSWORD
```
___

# Start

- Clone the repository.
```sh
$ git clone https://github.com/rahuladitya303/Library-Managament-System.git
$ cd Library-Management-System
```
- Create Virtual Environment.
```sh
$ virtualenv venv
$ source venv/bin/activate
```
- Install dependencies.
```sh
$ pip install -r requirements.txt --upgrade
```
- Run the application.
```sh
$ export FLASK_APP = runserver.py
$ flask run 
```
- Navigate to http://127.0.0.1:5000/  

**You can also used the included shell [script](https://github.com/rahuladitya303/Library-Managament-System/blob/master/start.sh).**
```sh
$ ./start.sh
```
# Project made and maintained by [Kumar Aditya](https://www.github.com/rahuladitya303)
