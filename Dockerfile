FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
COPY . /code/
WORKDIR /code

RUN pip install --upgrade pip wheel setuptools pipenv
RUN pipenv install
