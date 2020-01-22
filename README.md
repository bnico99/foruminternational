Build and Deploy
================

Since our implementation uses python, there is no need to compile our
code. For that reason, we do not strictly differentiate between
*building* and *deploying* our project. We will describe how to run our
project on a Ubuntu 19.04 (64-bit) local machine, but running it on a
server or different systems should work analogously. Please note that we
assume that you already have a running database. For information about
how to get your database running, please have a look at the [Django
documentation](https://docs.djangoproject.com/en/2.2/topics/install/#database-installation).

In order to run our project, follow these steps:

-   Check that you have at least python3.7 installed by running
    `python3 --version`. If not, execute `apt-get install python3.7`.

-   Check that you have at least pip19.3.1 installed by running
    `python3 -m pip --version`. If not, go to
    <https://pip.pypa.io/en/stable/installing/> and follow the
    instructions.

-   Execute
    `git clone https://github.com/bnico99/foruminternational.git mywebsite`.

-   Go to `mywebsite`.

-   Execute `python3 -m pip install -r requirements.txt` to install all
    requirements.

-   Open `website/settings.py`. For **local developement**, you can
    leave all settings unchanged (except `SECRET_KEY` and the `EMAIL`
    settings). For **use in production**, **definitely** check the
    following values:

    -   `SECRET_KEY`: Set this to a large **random** value and **keep it
        secret**.

    -   `DEBUG`: Set this to `FALSE`. Also make sure to read the
        following bullet points when doing this.

    -   `ALLOWED_HOSTS`: Set this to all hosts that should be allowed to
        access your website. Also check the [Django
        documentation](https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts)
        for this.

    -   `DATABASES`: Enter your database name and credentials there.
        Also check the [Django
        documentation](https://docs.djangoproject.com/en/2.2/ref/settings/#databases)
        for this.

    -   `EMAIL_x`: Enter mail host and account that your mails should be
        send from.

    Of course you should also check the other settings to adapt them to
    your needs, but they are not critical and we therefore kindly ask
    you to follow the [Django
    documentation](https://docs.djangoproject.com/en/2.2/ref/settings/)
    here. Please also make sure to have a look at the [**Deployment
    checklist**](https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/)
    provided in the Django documentation when running the project in
    production. Run `manage.py check --deploy` to automatically check
    some settings.

-   Since static files will be served by your web server (e.g. Apache)
    and not by Django itself anymore when you set `DEBUG=True`, you need
    to replace all occurences of `{% static 'xyz' %}` with the
    corresponding path on your web server when running in production
    with `DEBUG=True`.

-   After checking your configuration, execute
    `python3 manage.py migrate` to automatically create the needed
    database tables and to load some initial data.

-   Execute `python3 manage.py createsuperuser` and follow the dialogue
    to create a superuser that you can later use to access the admin
    interface on your website.

-   Finally, execute `python3 manage.py runserver` to start your server.
    Usually it will run at `localhost:8000`, but the executed
    `manage.py` script will also tell you where it is running.

-   Go to `localhost:8000/admin` and add the Cookie Consent instance by
    clicking "Hinzufügen" at "Cookie consent settingss" and
    configure it according to your wishes.

-   You can now use and discover your website. Have fun!

-   To quit the server, press `CTRL + C`.

When running in production, you also have to periodically execute some
scripts (via your server's cron):

-   `python3 manage.py remind_customers`: This script is responsible for
    sending reminder mails to customers when they have not paid the rent
    yet and only three days are left to the event date. Therefore, this
    script needs to be executed **once per day**.

-   `python3 manage.py create_blockers`: This script is responsible to
    create the blockers on weekdays (8-16h) for the next five years.
    Therefore, this script theoretically only needs to be run once in
    4,5 years, but since it does not duplicate existing blockers and is
    executed really fast, you can also run it on a more regular basis
    (e.g. also once per day).

Before running production, you should also adjust the mail templates,
contract, bills etc to your needs. This can be done by editing the
templates in the `templates` folder (e.g. `/templates/mails`) or the
document templates in the `data` folder.

Testing
=======

We have also delivered some tests to test the basic functionality of our
website. We have included unit tests and functional tests. Please make
sure that you have installed all requirements before executing the
tests. Moreover, you need to download `geckodriver` from [Mozilla's
GitHub](https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz)
and copy the file included in the `.tar.gz` archive to
`mywebsite/functional_tests`.

After that, executing the tests is fairly easy: You can run all tests by
executing `python3 manage.py test` in the `mywebsite` folder. You can
also run tests for a single app by executing
`python3 manage.py appname`, e.g.
`python3 manage.py booking` or `python3 manage.py functional_tests`.
