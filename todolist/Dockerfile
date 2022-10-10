FROM python:3.10-slim

WORKDIR /todolist_code/todolist
ENV PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.1

RUN apt update && apt full-upgrade -y && apt install gunicorn -y && apt autoremove -y

RUN pip install -U pip setuptools

# Dependencies installation with pip
#COPY requirements.txt .
#RUN pip install -r requirements.txt

# Dependencies installation with poetry
COPY poetry.lock pyproject.toml ./
RUN pip install "poetry==$POETRY_VERSION" -v
RUN POETRY_VIRTUALENVS_CREATE=false poetry install -v

COPY . .

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# not working, idk why
CMD ["gunicorn", "todolist.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "info", "--workers", "4"]
