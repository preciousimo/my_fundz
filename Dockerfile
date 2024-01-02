ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Combine COPY commands to reduce layers.
COPY requirements.txt /tmp/requirements.txt
COPY . /code

RUN set -ex && \
    pip install --upgrade pip && \
    pip install --verbose -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# Set the SECRET_KEY environment variable.
ENV SECRET_KEY "MDoBUbH87qPxp7nmy2yY82D5BMTjkhDMC90D9sZD66NDfvMx0f"

# Commented out temporarily for debugging.
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "my_fundz.wsgi"]
