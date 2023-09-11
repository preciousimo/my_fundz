ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "fr1%69mb8lejom$wqcx287^xhrso6fr@0$27xhw&q&m)8u&@j0"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Add uWSGI package installation
RUN pip install gunicorn

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "my_fundz.wsgi"]
