web: gunicorn app:app
init: flask db init
migrate: flask db migrate
upgrade: sh -c 'cd ./app/ && flask db upgrade'
