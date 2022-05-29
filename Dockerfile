FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install fastapi
RUN pip install uvicorn[standard]
RUN pip install google-cloud-firestore
RUN pip install websocket
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app