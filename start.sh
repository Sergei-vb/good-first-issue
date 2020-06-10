while ! nc -z $DATABASE_HOST $DATABASE_PORT; do sleep 1; done;

cd /poetry-env && poetry run python /gfi/app/main.py
