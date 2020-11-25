FROM python:3.7-alpine
WORKDIR /server
ENV APP_SETTINGS="backend.config.DevelopmentConfig"
ENV FLASK_APP="server.py"
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache postgresql-libs && \
      apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk --purge del .build-deps
EXPOSE 5000
COPY . .
CMD ["gunicorn", "server:app",  "-b", ":5000", "-k", "eventlet", "--log-level", "DEBUG"]
