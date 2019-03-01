# Use an official Python runtime as a parent image
FROM python:3

LABEL maintainer="Alexander Smith <arosmith3@gmail.com>"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
CMD ["python3", "regression.py"]
