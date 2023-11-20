DOCK_COMP = ./srcs/docker-compose.yml

all: build
	docker-compose -f $(DOCK_COMP) up -d
	# python3 ft_transcendence/manage.py runserver

build:
	mkdir -p ./srcs/data/db
	mkdir -p ./srcs/data/django
	docker-compose -f $(DOCK_COMP) up --build

clean:
	-docker-compose -f $(DOCK_COMP) down -v

fclean: clean
	-docker rmi srcs-db
	-docker rmi srcs-django
	# docker volume rm db
	# docker volume rm django

re: fclean all

reset:
	rm -rf ./data/postgresql
