build:
	docker compose -f docker-compose-local.yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose-local.yml up -d

down:
	docker compose -f docker-compose-local.yml down

down-v:
	docker compose -f docker-compose-local.yml down -v

config:
	docker compose -f docker-compose-local.yml config

makemigrations:
	docker compose -f docker-compose-local.yml run -rm api python manage.py makemigrations

migrate:
	docker compose -f docker-compose-local.yml run -rm api python manage.py migrate

collectstatic:
	docker compose -f docker-compose-local.yml run -rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f docker-compose-local.yml run -rm api python manage.py createsuperuser

flush:
	docker compose -f docker-compose-local.yml run -rm api python manage.py flush

db:
	docker compose -f docker-compose-local.yml exec postgres psql --username=root --dbname=finnect