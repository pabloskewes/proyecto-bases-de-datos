FROM python:3.9.2-slim-buster

COPY requirements.txt /tmp/requirements.txt

RUN pip install pip --upgrade && \
    pip install -r /tmp/requirements.txt --no-cache-dir

COPY project_logger/ ./project_logger
RUN pip install -e ./project_logger

COPY frontend/ ./frontend

WORKDIR /frontend

EXPOSE 8090

CMD ["python", "app.py"]
