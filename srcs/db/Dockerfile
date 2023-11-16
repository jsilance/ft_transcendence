FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
	postgresql \
	postgresql-contrib \
	postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

COPY ./srcs/db/psql_setup.sh /tmp/
COPY ./srcs/db/psql_setup.sql /tmp/
RUN chmod +x /tmp/psql_setup.sh

EXPOSE 5432

CMD ["/tmp/psql_setup.sh"]