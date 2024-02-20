DOCK_COMP = ./srcs/docker-compose.yml

all: build
	docker-compose -f $(DOCK_COMP) up -d

build:
	mkdir -p ./srcs/data/db
	# chmod 777 ./srcs/data/db
	docker-compose -f $(DOCK_COMP) up --build

clean:
	-docker-compose -f $(DOCK_COMP) down -v

fclean: clean
	-docker rmi postgres
	-docker rmi srcs-django
	-docker rmi srcs_django

reset: fclean
	rm -rf ./srcs/data
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf ./srcs/django/ft_transcendence/threejs

re: fclean all

.PHONY: all build clean fclean re reset