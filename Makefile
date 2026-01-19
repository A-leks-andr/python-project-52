install:
	pip install uv
	pip install gunicorn uvicorn
	uv venv
	uv pip install -r requirements.txt

sync:
	uv sync

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --no-input

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

shell:
	uv run manage.py shell