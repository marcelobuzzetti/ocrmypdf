# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 5000
ENV HOST 0.0.0.0
# Create and set the working directory in the container
WORKDIR /app

# Copy your Flask application code into the container
COPY . /app/

RUN ls -lha

# Install python dependencies
RUN pip install -r requirements.txt

# Expose the port your Flask app will run on
EXPOSE 5000

RUN FLASK_APP=main.py

# Command to run the Flask application
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "main:app"]

