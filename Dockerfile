FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN python manage.py collectstatic
RUN python manage.py migrate
RUN python manage.py setup_demo

EXPOSE 8000

CMD ["sh", "start.sh"]
