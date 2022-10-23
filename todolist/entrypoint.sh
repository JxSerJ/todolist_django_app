#!/bin/bash

python manage.py collectstatic --no-input -v 1
python manage.py migrate
exec "$@"
