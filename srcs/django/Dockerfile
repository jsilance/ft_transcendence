FROM debian:bookworm

RUN apt-get update -y && apt-get upgrade

RUN apt-get install python3 -y

# RUN sudo apt-get install python3-dev -y

COPY ./ft_transcendence /serv

CMD [ "python3", "ft_transcendence/manage.py", "runserver" ]
