install:
	pip install -r requirements.txt

migrate:
	python3 manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn hexlet_code.wsgi

test:
	PYTHONPATH=. pytest task_manager/tests -vv --ds=hexlet_code.settings