FROM python:3.9.2-slim-buster

COPY backend/requirements.txt /tmp/requirements.txt

RUN pip install pip --upgrade && \
    pip install -r /tmp/requirements.txt --no-cache-dir

COPY project_logger/ ./project_logger
RUN pip install -e ./project_logger

COPY backend/ ./backend

WORKDIR /backend

EXPOSE 8091

CMD ["python", "main.py"]
