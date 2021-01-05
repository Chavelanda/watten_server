FROM python:3.6

WORKDIR usr/src/flask_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:$PORT wsgi:server