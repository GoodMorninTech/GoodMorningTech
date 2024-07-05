# Use the official Python image from the Docker Hub
FROM python:3.11-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

RUN touch /var/log/cron.log && chmod 0644 /var/log/cron.log

RUN python -m flask --app gmt crontab add

RUN service cron start

# Expose the port the app runs on
EXPOSE 5000

# Run the command on container startup
CMD gunicorn -b 0.0.0.0:5000 index:app