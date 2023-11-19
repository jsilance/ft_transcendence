FROM debian:bookworm

RUN apt-get update && apt-get install -y \
	postgresql \
	postgresql-contrib

# RUN echo here

# COPY ./srcs/psql_setup.sh /tmp/
# COPY ./srcs/db/srcs/psql_setup.sql /tmp/
# RUN chmod +x /tmp/psql_setup.sh

# CMD ["/tmp/psql_setup.sh"]
CMD ["postgres", "-D", "/serv/data"]
