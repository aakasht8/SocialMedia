# Use the official Python image.
FROM python:3.9

# Set the working directory to /code.
WORKDIR /code

# Copy the requirements file into the container at /code.
COPY requirements.txt /code/

# Install the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code.
COPY . /code/

# Copy the wait-for-it script into the container and make it executable.
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Define environment variable.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run migrations and start the Django development server, but wait for the database to be ready first.
CMD ["sh", "-c", "/wait-for-it.sh db python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
