# Macalicious E-Commerce Website

A ecommerce website built in Python Django that enables customers to place orders, manage their orders and more.

The project has the following features:

- User Accounts
- Cart
- Contact
- Newsletter
- Orders
- Search
- Shop

## Installation

Create a python virtual environment.

```sh
python3 -m venv env
```

Clone the repository and name the folder `src`.

```sh
gh repo clone Elmer-Almeida/macalicious src
# OR
https://github.com/Elmer-Almeida/macalicious.git src
```

In the `src` folder run the following command to install all dependencies required:

```sh
pip3 install -r requirements.txt
```

Create an `.env` file with the following variables:

```sh
# Google reCaptcha configuration
GOOGLE_RECAPTCHA_SITE_KEY = "<value>"
GOOGLE_RECAPTCHA_SECRET_KEY = "<value>"

# Email configuration
EMAIL_HOST_USER = "<value>"
EMAIL_HOST_PASSWORD = "<value>"
EMAIL_USE_TLS = "<value>"
EMAIL_PORT = "<value>"
EMAIL_HOST = "<value>"

# Site admin configuration
ADMIN_NAME = "<value>"
ADMIN_EMAIL = "<value>"

# AWS S3 configuration
AWS_S3_HOST = "<value>"
AWS_ACCESS_KEY_ID = "<value>"
AWS_SECRET_ACCESS_KEY = "<value>"
AWS_STORAGE_BUCKET_NAME = "<value>"
AWS_S3_REGION_NAME = "<value>"

# PostgreSQL configuration
DATABASE_NAME = "<value>"
DATABASE_USER = "<value>"
DATABASE_PASSWORD = "<value>"
DATABASE_HOST = "<value>"
DATABASE_PORT = "<value>"
```

Make sure the `DEBUG` property in `src/macalicious/settings.py` is set to the desired setting.

```python
DEBUG = True   # for development
DEBUG = False  # for production
```

Make sure the `DEBUG_EMAIL` property in `src/macalicious/settings.py` is set to the desired setting:

```python
DEBUG_EMAIL = True   # will use dummy email backend
DEBUG_EMAIL = False  # will use live email service. NOTE: make sure email config is set in `.env`
```

Make sure you have a `db.sqlite3` file in the `src` folder if you will be using `DEBUG = True`

Once all dependencies are installed, run the following commands in the `src` folder:

```sh
# create migrations (if any)
python manage.py makemigrations

# migrate migrations
python manage.py migrate
```

To run a server on `http://localhost:8000`, run:

```sh
python manage.py runserver
```

## Heroku Deployment

Make sure `DEBUG` is set to `False` in the `src/macalicious/settings.py` file.

Run the following commands to deploy to heroku:

```sh
# check/create any migrations
heroku run --app macalicious python manage.py makemigrations

# migrate any migrations
heroku run --app macalicious python manage.py migrate
```

## Contact

Send me an email at: [almeielm@sheridancollege.ca](mailto:almeielm@sheridancollege.ca)
