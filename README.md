# thankloganforserving.us
Thanks Logan!

## Setup for Dev
Clone the repo, set up a `venv`, and run `python -m pip install -e ".[tests]"` to set up the dev environment.

### Useful Commands
`python manage.py migrate && python manage.py makemigrations thank_logan && python manage.py sqlmigrate thank_logan 0001 && python manage.py migrate &&  python manage.py createsuperuser && clear && python manage.py runserver`
