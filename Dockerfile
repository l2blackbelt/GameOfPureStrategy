# Use an official Python runtime as a parent image
FROM python:3

LABEL maintainer="Alexander Smith <arosmith3@gmail.com>"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ENV GIT_REPO="git@github.com:l2blackbelt/GameOfPureStrategy.git"
ENV GIT_BRANCH="master"
ENV GIT_ORIGIN="origin"
ENV COMMIT_USER="l2blackbelt"
ENV COMMIT_EMAIL="arosmith3@gmail.com"
ENV WORKING_DIR="."
ENV SSH_KEY=".ssh/id_rsa"
ENV FILES_TO_COMMIT="."



# Run app.py when the container launches
CMD ["python3", "regression.py"]
#RUN ["python3", "regression.py", "-v", "`pwd`:`pwd`", "-w", "`pwd`", "-i", "-t"]



COPY entrypoint.sh /entrypoint.sh
CMD ["/bin/sh","/entrypoint.sh"]


#copy results back to local filesystem
#COPY /app/outfile.txt .
#COPY /app/bot_scores.md .