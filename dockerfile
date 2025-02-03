# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install paho-mqtt python-dotenv

# Copy the .env file into the container
COPY .env .env

# Run the Python script when the container launches
CMD ["python", "dabo.py"]