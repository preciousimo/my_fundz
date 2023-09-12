# Use the official Python image as a parent image
FROM python:3.11-slim-bullseye

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Install psycopg2 dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for your code
RUN mkdir -p /code

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container at /tmp/requirements.txt
COPY requirements.txt /tmp/requirements.txt

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code

# Set the SECRET_KEY environment variable with quotes
ENV SECRET_KEY="1%fr69mb8lejom$wqcx287^xhrso6fr@0$x27hw&q&m)8u&@j0"

# Set the working directory to the Django project directory
WORKDIR /code/my_fundz

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Install gunicorn
RUN pip install gunicorn

# Specify the command to run gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers=2", "my_fundz.wsgi:application"]
