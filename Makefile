install:
	pip install uv
	pip install gunicorn uvicorn
	uv venv
	uv pip install -r requirements.txt

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

render-start:
	uv run manage.py migrate
	uv run gunicorn task_manager.wsgi:application

start:
	uv run manage.py runserver

update-css:
	uv run manage.py collectstatic --noinput

shell:
	uv run manage.py shell