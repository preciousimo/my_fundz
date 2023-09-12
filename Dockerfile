
ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTE CODE1
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
    rm -rf /root/./
# Fixed typo: Removed extra "cache" from COPY command
COPY . /code

# Add quotes to the SECRET_KEY environment variable
# Fixed typo: Added missing space after "=" sign
ENV SECRET_KEY "fr1%69mb8lejom$wqcx287^xhrso6fr@0$27xhw&q&m)8u&@j0"

# Collecting static files
# Fixed typo: Changed "manage.py" to "./manage.py" in the command
RUN python ./manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Add uWSGI package installation
RUN pip install gunicorn

# Use the CMD instruction with double quotes to properly specify the command and arguments
CMD ["gunicorn", "--bind", ":8000", "--workers=2", "my_fundz.wsgi"]
