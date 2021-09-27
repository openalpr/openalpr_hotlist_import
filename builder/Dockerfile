from ubuntu:18.04
RUN apt-get update && apt-get install -y \
    libmysqlclient-dev \
    libffi-dev \
    python-dev \
    libjpeg-dev \
    python3-pip \
    git \
    nsis
RUN pip3 install pynsist
RUN apt-get clean
