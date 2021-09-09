FROM python:3.8
LABEL maintainer chris@shenkan.dev

ENV DJANGO_SETTINGS_MODULE=eatplants.settings.dev

WORKDIR /app

COPY manage.py /app/
COPY requirements/ /app/requirements

RUN pip install -r requirements/dev.txt

COPY config config
COPY eatplants eatplants
COPY accounts accounts
COPY articles articles
COPY templates templates

ADD /scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/usr/local/bin/gunicorn", "--config", "config/gunicorn.py", "--log-config", "config/logging.conf", "-e", "DJANGO_SETTINGS_MODULE=eatplants.settings.dev", "-w", "4", "-b", "0.0.0.0:8001", "eatplants.wsgi:application"]

