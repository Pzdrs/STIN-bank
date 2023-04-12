FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["celery", "-A STINBank", "worker", "-l", "INFO"]

CMD ["celery", "-A STINBank", "beat", "-l", "INFO"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["python", "manage.py", "createsuperuser", ""]