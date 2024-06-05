# Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENV INSTANCE='1'

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api.wsgi:application"]