FROM python:3.8-slim-buster

# copy files into /code directory
COPY . /code
# make directory /code as working directory
WORKDIR /code
# install python packages from requirements.txt
RUN pip install -r requirements.txt
