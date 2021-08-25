FROM python:3.9

WORKDIR /usr/projects/alarmbot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt update apt install postgresql-dev gcc python3-dev musl-dev
RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y
RUN apt-get upgrade -y && apt-get install dos2unix


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .

RUN dos2unix /usr/projects/alarmbot/entrypoint.sh

RUN chmod +x /usr/projects/alarmbot/entrypoint.sh

ENTRYPOINT ["/usr/projects/alarmbot/entrypoint.sh"]












#FROM python:3.8
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#WORKDIR /usr/src
#
#COPY ./requirements.txt /usr/src/requirements.txt
#RUN pip install -r /usr/src/requirements.txt
#
#COPY . /usr/src
#
#EXPOSE 8000