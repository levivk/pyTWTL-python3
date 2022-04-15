FROM ubuntu:18.04

RUN apt-get update && apt-get install git curl binutils python2.7-dev -y

# install pip
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py | python2.7

# Copy things

COPY src b/src
COPY lib b/lib
COPY data b/data
COPY requirements.txt b/requirements.txt
COPY twtl_translate.spec b/twtl_translate.spec

# Install python requirements
RUN python2.7 -m pip install -r b/requirements.txt

# Build
RUN cd b && pyinstaller twtl_translate.spec


