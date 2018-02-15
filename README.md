# README #

This readme will guide you to setup your project

### What is this repository for? ###

App to list repositories for public organizations at Github using the Github API "V3"
This project was made as code challenge to Blizuu by A. González

### How do I get set up? ###

1. run dependencies
`pip install -r requirements.txt`

2. Config your .env file

    Open the file .env.base and rename (don't delete) as .env
    Here you should configure your app database and the rest os project settings that haven't hardcode in settings/base.py or any other setting file

    OPTIONAL:
        
        At this point is very important to notice you that if you want to increase your GITHUB Api Rates, you may create an test app in to you github account, accesssing to Settings ->Developer settings -> OAuth Apps and once you've created your app, add your app CLIEND_ID and app CLIENT_SECRET in your .env file as follow:
        
        GITHUB_CLIENT_ID=YOUR_APP_CLIEND_ID

        GITHUB_CLIENT_SECRET=YOUR_APP_CLIEND_SECRET

3. Run migrations

* 3.1 `python manage.py makemigrations`
* 3.2 `python manage.py migrate`

4. Create superuser
`python manage.py createsuperuser`


### Contribution guidelines ###

* Writing tests
Write your test under a tests folder in each app folder if it's possible

Run your tests as follow
`python manage.py test`


### Who do I talk to? ###

* Don't hesitate to contact me by the email: afgonzalezgarcia@gmail.com
