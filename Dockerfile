FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install Flask gunicorn
RUN pip install google-cloud-firestore
RUN pip install requests
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app