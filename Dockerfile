# Use an official OCRMYPDF runtime as a parent image
FROM python:3.10-slim-buster

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
RUN apt install ocrmypdf tesseract-ocr-por automake libtool libleptonica-dev git -y
RUN git clone https://github.com/agl/jbig2enc \
cd jbig2enc \
./autogen.sh \
./configure && make \
sudo make install

# Expose the port your Flask app will run on
EXPOSE 8080

RUN FLASK_APP=main.py

# Command to run the Flask application
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "main:app"]

