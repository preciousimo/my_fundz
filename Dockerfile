
PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1  # Set PYTHONDONTWRITEBYTECODE to 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set - \
ex &&    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/  # Removed the extra dot (typo)

COPY . /code

ENV SECRET_KEY="fr1%69mb8lejom$wqcx287^xhrso6fr@0$x27hw&q&m)8u&@j0"  # Added quotes to the SECRET_KEY environment variable

RUN python manage.py collectstatic --noinput  # Corrected the path to 'manage.py'

EXPOSE 8000

RUN pip install gunicorn  # Installed gunicorn package

CMD ["gunicorn", "--bind", ":8000", "--workers=2", "my_fundz.wsgi"]  # Set the command and arguments for gunicorn using double quotes
