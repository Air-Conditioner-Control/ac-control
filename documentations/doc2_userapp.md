# User App

## Creating New Branch

	$ git checkout -b 1_user_app


## Migrations
	$ python3 manage.py makemigrations
	$ python3 manage.py migrate

## Creating home app
	$ python3 manage.py startapp home
## Copy all Home app from ac_control
And adjust the settings, urls.



## Create super user

	$ python3 manage.py createsuperuser
	
Check the created super user by
	
	$ python3 manage.py runserver

and try login in the admin page http://localhost:8000/admin/


## Create User App

	$ python3 manage.py startapp users

## Copy all User app from dataholic
And adjust the settings, urls.

migrate user app model
	
	$ python3 manage.py makemigrations
	$ python3 manage.py migrate


## Creating profile for superuser
	
	$ python3 manage.py shell
in the shell

Import neccesary model

	>>> from django.contrib.auth.models import User
	>>> from users.models import Profile

Get the super user objects

	>>> u = User.objects.all()
	>>> u
	>>> u1 = u[0]
	>>> u1

Create profile for the superuser

	>>> p = Profile(user=u1)
	>>> p
	>>> p.save()
	>>> exit()

and test about register, login, logout, profile and updateing profile.

## Push the changes

	$ git add .
	$ git commit -m "Creating super user."
	$ git push --set-upstream origin 1_user_app


## Merging to main branch

	$ git checkout main
	$ git pull origin 1_user_app
	$ git push

