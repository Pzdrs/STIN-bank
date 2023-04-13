FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN python manage.py collectstatic
RUN python manage.py migrate
RUN python manage.py create_default_admin

EXPOSE 8000

CMD ["sh", "start.sh"]
