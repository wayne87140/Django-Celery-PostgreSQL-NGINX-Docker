#!/bin/sh

# wait for PSQL server to start
sleep 10

sh -c "celery -A model1 worker -l info"