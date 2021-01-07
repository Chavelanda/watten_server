FROM python:3.6

WORKDIR usr/src/flask_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 5000

COPY . .

ENV  APP_SETTINGS="config.ProductionConfig"

ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh"]
