FROM python:3.6.12 

ENV PYTHONUNBUFFERED 1 \ PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt .
RUN pip install pip -U &&\
    pip install -r requirements.txt

RUN mkdir -p /home/proj &&\
    mkdir /home/proj/web &&\
    mkdir /home/proj/web/static &&\
    mkdir /home/proj/web/media &&\
    groupadd -r HELLOWORLD &&\
    useradd -r -g HELLOWORLD -d /home/proj HELLOWORLD 

WORKDIR /home/proj/web

COPY . /home/proj/web

RUN chown -R HELLOWORLD:HELLOWORLD /home/proj/web

USER HELLOWORLD