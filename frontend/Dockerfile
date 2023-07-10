FROM python:3.9.2-slim-buster

COPY frontend/requirements.txt /tmp/requirements.txt

RUN pip install pip --upgrade && \
    pip install -r /tmp/requirements.txt --no-cache-dir

COPY project_logger/ ./project_logger
RUN pip install -e ./project_logger

COPY frontend/ ./frontend

WORKDIR /frontend

EXPOSE 8090

CMD ["gunicorn", "app:server", "-w", "3", "--bind", "0.0.0.0:8090", "--timeout", "300"]
# CMD ["python", "app.py"]
