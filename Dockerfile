FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install responder --pre
RUN pip install google-cloud-firestore
RUN pip install websocket
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app