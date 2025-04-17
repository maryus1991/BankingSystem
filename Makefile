build:
    docker compose -f docker-compose-local.yml up --build -d --remove-orphans

up:
    docker compose -f  docker-compose-local.yml up -d

down:
    docker compose -f docker-compose-local.yml down

down-v:
    docker compose -f docker-compose-local.yml down -v

banker-config:
    docker compose -f docker-compose-local.yml config

makemigrations:
    docker compose -f docker-compose-local.yml run --rm api python manage.py makemigrations
migrate:
    docker compose -f docker-compose-local.yml run --rm api python manage.py migrate

collectstatic:
    docker compose -f docker-compose-local.yml run --rm api python manage.py collectstatic

superuser:
    docker compose -f docker-compose-local.yml run --rm api python manage.py superuser

flush:
    docker compose -f docker-compose-local.yml run --rm api python manage.py flush

network-inspect:
    docker network inspect banker_local_nw

banker-db:
    docker compose -f docker-compose-local.yml exec postgres psql --username=root --dbname=banker