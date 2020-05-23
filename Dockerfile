FROM python:3.6

MAINTAINER Ruturaj Mohite

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt
RUN pip install django-autocomplete-light
RUN pip install whitenoise

COPY . /app

RUN python3 manage.py migrate

EXPOSE 8000

ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000
