FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip wheel setuptools pipenv
RUN pipenv install

COPY . /code/
