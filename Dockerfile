# Use an official python runtime as a parent image
FROM python:3.10-buster

# Select SHELL
SHELL ["/bin/bash", "-c"] 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080
ENV HOST 0.0.0.0

# Create and set the working directory in the container
WORKDIR /app

# Copy your Flask application code into the container
COPY . /app/

RUN ls -lha

# Install python dependencies
RUN pip install -r requirements.txt

#Install OCRMYPDF
RUN apt update
RUN apt install ocrmypdf tesseract-ocr-por -y


# Expose the port your Flask app will run on
EXPOSE 8080

RUN FLASK_APP=main.py

# Command to run the Flask application
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "main:app", "--timeout 600"]

