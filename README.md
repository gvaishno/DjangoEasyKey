# UserList with PII
### With Randtronics DPM easyKey capabilities.
### Developed merely for demonstrations. Not for production.

## Deployment
### Prerequisite
1. Python3
2. Git
3. OS - Linux/ Windows
### Get the code.
```
git clone https://github.com/gvaishno/User-PII-List
cd User-PII-List
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Configure the server
Example configuration in settings.py file.
```
# MYSQL DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'userlist',
        'USER': 'remote',
        'PASSWORD': 'remote',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

RANDTRONICS_EASYKEY_API = "https://localhost:8943"
RANDTRONICS_EASYEKEY_AUTH_KEY = "Y2xpZW50OjEyMw=="
```
### Run the server
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
