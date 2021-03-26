# docker build -t local/git2dot -f docker/Dockerfile .

# Inspiration : https://www.docker.com/blog/containerized-python-development-part-1/
# https://towardsdatascience.com/conda-pip-and-docker-ftw-d64fe638dc45

# first stage

# set base image (host OS)
FROM debian:stable AS base

MAINTAINER Olivier Berger <olivier.berger@telecom-sudparis.eu>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update

RUN apt-get -y install \
    python3 \
    python3-pip \
    git

# Select Python 3 by default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Create a non-root user
ARG username=al-khawarizmi
ARG uid=1000
ARG gid=100
ENV USER $username
ENV UID $uid
ENV GID $gid
ENV HOME /home/$USER
RUN adduser --disabled-password \
    --gecos "Non-root user" \
    --uid $UID \
    --gid $GID \
    --home $HOME \
    $USER

# -----------
# Second stage : build 
FROM base as builder

# Nothing to install anymore
#RUN apt-get -y install \

USER $USER

# set the working directory in the container
RUN mkdir /home/$USER/git2dot

WORKDIR /home/$USER/git2dot

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install --user -r requirements.txt

COPY Makefile .
COPY utils/ ./utils
COPY setup.py .
COPY git2dot ./git2dot
COPY README.rst .

# -----------
# Last unnamed stage : runtime

FROM base

RUN apt-get -y install \
    make \
    graphviz

# copy only the built elements and not all intermediary utilities installed into .local by pip
COPY --from=builder /home/$USER/git2dot /home/$USER/git2dot
RUN chown -R $UID:$GID /home/$USER/git2dot

# Install the execution entry point script
COPY docker/entrypoint.sh /usr/local/bin/
RUN chown $UID:$GID /usr/local/bin/entrypoint.sh && \
    chmod u+x /usr/local/bin/entrypoint.sh

USER $USER

WORKDIR /home/$USER/git2dot

RUN make V=1 install

# update PATH environment variable
ENV PATH=/home/$USER/.local/bin:$PATH

#SHELL [ "/bin/bash", "--login", "-c" ]

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

# command to run on container start
CMD [ "git2dot", "-h" ]
