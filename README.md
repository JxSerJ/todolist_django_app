# Django 4 project
___
**Title:** ToDo List App \
**Description:** To do list application based on Django 4.1.1.


### Functionality:
- [ ] none / under development


### Main components:

    - Python 3.10.7
    - Django 4.1.1
    - Poetry 1.2.1
    - Postgresql (docker compose container, latest version)

###
### How to launch:

1. Create and activate Python 3.10.7 virtual environment
2. Install package manager Poetry:\
   `pip intall poetry`
3. Download and install project dependencies:\
   `poetry install`
4. Create docker compose container with postgresql db:\
   `docker compose up --build -d`\
    Project contains already prepopulated DB in `./database/` dir, but you can always create new one by deleting `./database/` folder.\
    All env-data for db creation stores in `.env` file in project root dir
5. If you use prepopulated project db **skip this step**.\
   In case of creation of your own db you'll need to perform migrations:\
   `python ./todolist/manage.py migrate`
6. Launch server:\
   `python ./todolist/manage.py runserver`

You can access django-admin panel from http://127.0.0.1:8000/admin/ 

Credentials for superuser are following (if you're using project db): 

**Login**: `admin`\
**Password**: `admin`




