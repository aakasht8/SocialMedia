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

# Define environment variable.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run migrations and start the Django development server.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
