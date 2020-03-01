# thankloganforserving.us
Thanks Logan!

## Enviroment Variables
The following environment variables must be defined for `thankloganforserving` to function.

**STATIC_ROOT**: The static root directory to serve static files out of.

**SMS_KEY**: The SIP.US SMS API key.

**LOGAN_CELL**: Logan's cell phone number.

**SECRET_KEY**: The Django secret key.

## Setup for Dev
Clone the repo, set up a `venv`, and run `python -m pip install -e ".[tests]"` to set up the dev environment.

### Useful Commands
`python manage.py migrate && python manage.py makemigrations thank_logan && python manage.py sqlmigrate thank_logan 0001 && python manage.py migrate &&  python manage.py createsuperuser && clear && python manage.py runserver`
