# Use an official Python runtime as a parent image
FROM python:3

LABEL maintainer="Alexander Smith <arosmith3@gmail.com>"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ADD /.ssh/id_rsa .
ADD /.ssh/known_hosts .

ENV GIT_REPO="git@github.com:l2blackbelt/GameOfPureStrategy.git"
ENV GIT_BRANCH="master"
ENV GIT_ORIGIN="origin"
ENV COMMIT_USER="Magic Auto-build"
ENV COMMIT_EMAIL="<>"
ENV WORKING_DIR="."
ENV FILES_TO_COMMIT="."



# Run app.py when the container launches
CMD python3 scoreboard.py; /bin/sh entrypoint.sh
