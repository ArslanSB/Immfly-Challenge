#!/bin/bash

# make a tmp file
TMPFILE=$(mktemp)

# install all the requirements
echo -ne "Installing requirements for django ..."
pip3 install -r build/requirements.txt &>${TMPFILE} && echo "[done]" || { echo "[failed]"; echo "Something went wrong, is the output of the command that failed: "; cat ${TMPFILE}; }

# generate static files before starting anything
echo -ne "Generating static files ... "
printf "yes\n" | python manage.py collectstatic &>${TMPFILE} && echo "[done]" || { echo "[failed]"; echo "Something went wrong, is the output of the command that failed: "; cat ${TMPFILE}; }

# get processor cores
CPUCORES=`getconf _NPROCESSORS_ONLN`
# GUNI_WORKERS=$((($CPUCORES*2+1)))
GUNI_WORKERS=$((($CPUCORES+1)))

echo "Starting gunicorn ..."
gunicorn api.wsgi:application --workers=${WORKERS:-$GUNI_WORKERS} --threads=${THREADS:-2} --worker-class=gthread --bind 0.0.0.0:3000
