FROM python:3.9.18-bookworm

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install postgresql-client -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir psycopg2-binary \
				django \
				djangorestframework \
				django-cors-headers

COPY ./ft_transcendence /home/django/ft_transcendence

WORKDIR /home/django/ft_transcendence

COPY ./launch.sh /home/django/launch.sh 

RUN chmod +x /home/django/launch.sh

EXPOSE 8000

CMD [ "/bin/bash", "/home/django/launch.sh" ]

# CMD [ "python3", "manage.py", "runserver" ]
