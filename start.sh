while ! nc -z $DATABASE_HOST $DATABASE_PORT; do sleep 1; done;

poetry run python app/main.py
