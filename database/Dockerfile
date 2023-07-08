FROM postgres:13

COPY database/data/*.csv data/
COPY database/init.sql ./docker-entrypoint-initdb.d/

EXPOSE 5432
