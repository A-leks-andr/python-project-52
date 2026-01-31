install:
	pip install uv
	uv sync

sync:
	uv sync

migrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

collectstatic:
	uv run manage.py collectstatic --no-input

build:
	./build.sh

lint:
	uv run ruff check --fix

format:
	uv run ruff format

test:
	python manage.py test

render-start:
	uv run manage.py migrate
	uv run gunicorn task_manager.wsgi:application

start-server:
	python manage.py runserver 0.0.0.0:3000

update-css:
	uv run manage.py collectstatic --noinput

shell:
	uv run manage.py shell

start:
	uv run manage.py runserver