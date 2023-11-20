FROM debian:bookworm

RUN apt-get update -y && apt-get upgrade

RUN apt-get install python3 python3-pip python3-django -y

# RUN python3 -m pip install Django

# RUN sudo apt-get install python3-dev -y

COPY ./ft_transcendence /serv/data

WORKDIR /serv/data

CMD [ "python3", "manage.py", "runserver" ]
