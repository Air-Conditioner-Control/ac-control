# Github Organization Creation
## Create github organization for Air Conditioner Control
Got to the top-left and create organtization

## Create repositories
### Create ac_control

## Cloning the ac_control
	
	$ git clone github.com-Mujirin:Air-Conditioner-Control/ac_control.git

## Create Django Project
### Create Django project
	$ django-admin startproject ac_control

Place all the contained file in the project to the repo.

### Setingan rahasia
Remove the SECRET_KEY in the settings.py to to other file and add that file in the .gitignore

### Documentation
Create documentation folder to document anything


## Virtual Environment
### Creating a new virtual env 
Create in deployment in the project dir where the manage.py are in (ac_control folder):

	$ python3 -m venv venv


Activate it

	$ source venv/bin/activate

Upgrade the pip

	$ pip install --upgrade pip

Installing all requirements (add requirements.txt file on the project folder)

	$ pip install -r requirements.txt


### Run the development server

	$ python3 manage.py runserver

see on http://localhost:8000/


### Pull to the remote repo
	$ git status
	$ git add .
	$ git commit -m "Initial application."
	$ git push

### Notes
From Conda to Pip env
Source: https://stackoverflow.com/questions/50777849/from-conda-create-requirements-txt-for-pip3
