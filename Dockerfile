ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

RUN apt-get update && apt-get upgrade -y --no-install-recommends
RUN apt-get install -y ca-certificates wget

RUN apt-get install -y fontconfig libfreetype6 libjpeg62-turbo libpng16-16 libx11-6 libxcb1 libxext6 libxrender1 xfonts-75dpi xfonts-base
RUN wget -nv https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
RUN apt-get purge -y --auto-remove wget xz-utils \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm wkhtmltox_0.12.6.1-2.bullseye_amd64.deb

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

EXPOSE 8000

RUN [ "python3", "manage.py", "collectstatic", "--no-input", "-c"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "registro_atividades.wsgi"]
