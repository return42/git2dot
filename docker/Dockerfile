# docker build -t local/git2dot -f docker/Dockerfile .

# Inspiration : https://www.docker.com/blog/containerized-python-development-part-1/

# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
#COPY src/ .

# command to run on container start
#CMD [ "python", "./server.py" ]
