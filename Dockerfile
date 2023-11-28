ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

EXPOSE 8000

# Change before running the deploy command
ENV DJANGO_SUPERUSER_EMAIL=admin@admin.com 
ENV DJANGO_SUPERUSER_PASSWORD=admin

RUN [ "python3", "manage.py", "migrate" ]
RUN [ "python3", "manage.py", "createsuperuser", "--no-input" ]
RUN [ "python3", "manage.py", "collectstatic", "--no-input", "-c"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "registro_atividades.wsgi"]
