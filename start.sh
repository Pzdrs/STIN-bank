python manage.py runserver 0.0.0.0:8000
celery -A STINBank worker -l INFO
celery -A STINBank beat -l INFO
