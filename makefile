install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn hexlet_code.wsgi