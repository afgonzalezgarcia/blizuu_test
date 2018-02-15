# README #

This readme will guide you to setup your project

### BLIZUU TEST ###

This App lists repositories for public organizations at Github using the Github API "V3"

This project was made as code challenge to Blizuu by A. González

### How do I get set up? ###

1. run dependencies

   `pip install -r requirements.txt`

2. Config your .env file

    Open the file `.env.base` and rename (don't delete) as `.env`
    Here you should configure your app database and the rest os project settings that haven't hardcode in `settings/base.py` or any other setting file

    OPTIONAL:

    At this point is very important to notice you that if you want to increase your GITHUB Api Rates, you may create an test app in to you github account, accesssing to Settings ->Developer settings -> OAuth Apps and once you've created your app, add your app CLIEND_ID and app CLIENT_SECRET at the end of your .env file as follow:

    * GITHUB_CLIENT_ID=YOUR_APP_CLIENT_ID

    * GITHUB_CLIENT_SECRET=YOUR_APP_CLIENT_SECRET

    Documentation about:
    python-decouple: https://pypi.python.org/pypi/python-decouple
    dj-database-url: https://github.com/kennethreitz/dj-database-url

3. Run migrations

    * 3.1 `python manage.py makemigrations`
    * 3.2 `python manage.py migrate`

4. Create Superuser

    `python manage.py createsuperuser`

### Contribution guidelines ###

* Writing tests
1. Write your test under a folder called `tests` in each app folder

2. Config `pytest.ini` file

   Find  the file called `pytest.ini.base` in your project root folder, rename it (don't delete) to `pytest.ini`

   Open `pytest.ini` and place in the `DJANGO_SETTINGS_MODULE` settings, the path to your tests settings  (usually the same that your are using to the project)

3. Run your tests

    You can run your test simply using pytest

    `pytest`

    If you want to run your test and generates a coverage reporte, you have to run as follow

    `py.test --cov-report html:cov_html --cov=myapp/tests`

    The above example create a coverage report in HTML format located at the folder `cov_html` in your project root folder

    Documentation about:
    django-pytest: https://pytest-django.readthedocs.io
    pytest-con: https://pytest-cov.readthedocs.io/en/latest/

### Who do I talk to? ###

* Don't hesitate to contact me by the email: afgonzalezgarcia@gmail.com