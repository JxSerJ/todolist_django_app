FROM python:3.10-slim

WORKDIR /todolist_code/todolist
ENV PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.1 \
    PYTHON_PATH=/todolist_code/todolist \
    PYTHONUNBUFFERED=1

RUN apt update && apt full-upgrade -y && apt autoremove -y

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

ENTRYPOINT ["bash", "entrypoint.sh"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "todolist.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "debug", "--capture-output", \
         "--enable-stdio-inheritance", "--workers", "4", "--access-logfile", "gunicorn.log"]
