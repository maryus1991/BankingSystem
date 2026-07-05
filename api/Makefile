build:
	sudo docker compose -f local.yml up --build -d --remove-orphans

up:
	sudo docker compose -f local.yml up -d

down:
	sudo docker compose -f local.yml down

down-v:
	sudo docker compose -f local.yml down -v

banker-config:
	sudo docker compose -f local.yml config

makemigrations:
	sudo docker compose -f local.yml run --rm api sh -c "python manage.py makemigrations"

migrate:
	sudo docker compose -f local.yml run --rm api sh -c "python manage.py migrate"

collectstatic:
	sudo docker compose -f local.yml run --rm api sh -c "python manage.py collectstatic --no-input --clear"

superuser:
	sudo docker compose -f local.yml run --rm api sh -c "python manage.py createsuperuser"

flush:
	sudo docker compose -f local.yml run --rm api sh -c "python manage.py flush"

network-inspect:
	sudo docker network inspect banker_local_nw

banker-db:
	sudo docker compose -f local.yml exec postgres psql --username=maryus --dbname=banker