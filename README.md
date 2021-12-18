# Macalicious

This is the codebase for [Macalicious](https://www.macalicious.ca/). A website to showcase various Macaron cookies for
sale in Ontario.

The codebase has the following apps:

* Account
* Cart
* Contact
* Newsletter
* Orders
* Search
* Shop

## Installation

Download the codebase and in the **_src_** folder run the following command:

    # install all dependencies (python 3)
    pip3 install -r requirements.txt

Make sure the <code>DEBUG</code> property in <code>settings.py</code> is set to the desired settings.

Once all dependencies are installed, run the following commands in the **_src_** folder:

    # create migrations (if any)
    python manage.py makemigrations
    
    # migrate migrations
    python manage.py migrate

To run a server on <code>localhost:8000</code>, run:

    python manage.py runserver

### Heroku Deployment

Make sure <code>DEBUG</code> is set to <code>False</code> in <code>settings.py</code> file.

Run the following commands to get Heroku app up to speed:

    # check/create any migrations
    heroku run python manage.py makemigrations

    # migrate any migrations
    heroku run python manage.py migrate

### Contact

Any questions or concerns email me at <elmer.dev.95@gmail.com>