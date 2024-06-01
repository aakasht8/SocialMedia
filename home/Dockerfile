# Use the official Python image.
FROM python:3.9

# Set the working directory to /code.
WORKDIR /code

# Install the PostgreSQL client tools.
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt /code/

# Install the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code.
COPY . /code/

COPY wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh

# Define environment variable.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run migrations and start the Django development server.
CMD ["sh", "-c", "/wait_for_db.sh db python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
