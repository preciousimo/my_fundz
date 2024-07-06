# Base Image
FROM python:3.9-slim

# Environment Variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (if applicable)
RUN python manage.py collectstatic --no-input

# Expose port 8000
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "my_fundz.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]