install:
	uv sync

build:
	./build.sh

lint:
	uv run ruff check --fix

format:
	uv run ruff format

render-start:
	gunicorn task_manager.wsgi

start:
	uv run manage.py runserver 8080

update-css:
	python manage.py collectstatic --noinput