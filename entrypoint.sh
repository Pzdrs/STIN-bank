#!/bin/sh

python -m manage migrate --no-input
python -m manage collectstatic --no-input
python -m manage update_rates
python -m manage setup_demo

celery -A STINBank worker -l info &
celery -A STINBank beat -l info &

gunicorn STINBank.wsgi:application --bind 0.0.0.0:8000
