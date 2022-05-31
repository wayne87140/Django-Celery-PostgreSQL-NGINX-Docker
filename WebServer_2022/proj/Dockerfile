################### Build
FROM python:3.6.12 as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /usr/src/proj

RUN pip install pip -U
RUN pip install flake8
COPY . .
#RUN flake8 --ignore=E501,F401 ./


COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/proj/wheels -r requirements.txt


################### Final
FROM python:3.6.12

#ENV C_FORCE_ROOT true

RUN mkdir -p /home/proj

RUN groupadd -r HELLOWORLD &&\
    useradd -r -g HELLOWORLD -d /home/proj HELLOWORLD 

ENV HOME=/home/proj
ENV PROJ_HOME=/home/proj/web
ENV MPLCONFIGDIR /tmp/
RUN mkdir -p $PROJ_HOME
RUN mkdir -p $PROJ_HOME/static
#RUN mkdir -p $PROJ_HOME/media
WORKDIR $PROJ_HOME

COPY --from=builder /usr/src/proj/wheels /wheels
COPY --from=builder /usr/src/proj/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . $PROJ_HOME

#COPY ./run_web.sh /home/proj/web/run_web.sh/run_web.sh
#COPY ./run_celery_worker.sh /home/proj/web/run_celery_worker.sh
#COPY ./run_celery_beat.sh /home/proj/web/run_celery_beat.sh
#COPY ./entrypoint.sh /home/proj/web/entrypoint.sh

RUN chmod +x /home/proj/web/entrypoint.sh

RUN chown -R HELLOWORLD:HELLOWORLD $PROJ_HOME

USER HELLOWORLD

ENTRYPOINT ["/home/proj/web/entrypoint.sh"]