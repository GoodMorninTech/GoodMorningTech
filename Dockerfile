# Use the official Python image from the Docker Hub
FROM python:3.11-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Copy crontab file
COPY crontab /etc/cron.d/goodmorningtech-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/goodmorningtech-cron

# Apply cron job
RUN crontab /etc/cron.d/goodmorningtech-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Expose the port the app runs on
EXPOSE 5000

# Run the command on container startup
CMD cron && gunicorn -b 0.0.0.0:5000 index:app