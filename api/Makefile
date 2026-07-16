ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))


build:
	sudo docker compose -f local.yml up $(ARGS) --build -d --remove-orphans

up:
	sudo docker compose -f local.yml up $(ARGS) -d

ps:
	sudo docker compose -f local.yml ps $(ARGS) -a

down:
	sudo docker compose -f local.yml down $(ARGS)

restart:
	sudo docker compose -f local.yml restart $(ARGS)

down-v:
	sudo docker compose -f local.yml down $(ARGS) -v

logs-f:
	sudo docker compose -f local.yml logs -f $(ARGS)

log:
	sudo docker compose -f local.yml logs $(ARGS)

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

bash:
	sudo docker compose -f local.yml run --rm $(ARGS) sh

sh:
	sudo docker compose -f local.yml run --rm $(ARGS) sh

network-inspect:
	sudo docker network inspect banker_local_nw

banker-db:
	sudo docker compose -f local.yml exec postgres psql --username=maryus --dbname=banker
