FROM python:3.11-alpine

WORKDIR /app

RUN pip install --upgrade pip

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]
