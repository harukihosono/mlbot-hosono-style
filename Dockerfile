FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install fastapi
RUN pip install uvicorn[standard]
RUN pip install google-cloud-firestore
RUN pip install websocket
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]