DOCK_COMP = ./srcs/docker-compose.yml

all: build
	docker-compose -f $(DOCK_COMP) up -d
	# python3 ft_transcendence/manage.py runserver

build:
	mkdir -p ./data/postgresql
	docker-compose -f $(DOCK_COMP) build

clean:
	-docker-compose -f $(DOCK_COMP) down -v

fclean: clean

re: fclean all

reset:
	rm -rf ./data/postgresql
