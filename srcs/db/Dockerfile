FROM debian:bookworm

RUN apt-get update && apt-get install -y \
	postgresql \
	postgresql-contrib\
	sudo

RUN mkdir -p /serv/data
# RUN echo here

COPY ./srcs/psql_setup.sh /tmp/
# COPY ./srcs/db/srcs/psql_setup.sql /tmp/
RUN chmod +x /tmp/psql_setup.sh

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB django

CMD ["/bin/bash", "/tmp/psql_setup.sh"]

