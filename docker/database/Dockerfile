FROM postgres:13

COPY ./*.csv ./data/
COPY ./create_db.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_USER cc3201
ENV POSTGRES_ROOT_PASSWORD "ambashoyomote("
EXPOSE 5432
