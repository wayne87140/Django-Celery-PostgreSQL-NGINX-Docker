#!/bin/sh

# wait for PSQL server to start
sleep 15

sh -c "celery -A model1 beat -l info --pidfile=" 