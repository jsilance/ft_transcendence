DOCK_COMP = ./srcs/docker-compose.yml

all: build
	docker-compose -f $(DOCK_COMP) up -d
	# python3 ft_transcendence/manage.py runserver

build:
	mkdir -p ./srcs/data/db
	# mkdir -p ./srcs/data/django
	docker-compose -f $(DOCK_COMP) up --build

clean:
	-docker-compose -f $(DOCK_COMP) down -v

fclean: clean
	-docker rmi postgres
	-docker rmi srcs-django
	# docker volume rm postgres
	# docker volume rm django

rip: fclean
	rm -rf ./srcs/data

re: fclean all

reset: rip
	rm -rf ./data/postgresql

.PHONY: all build clean fclean rip re reset