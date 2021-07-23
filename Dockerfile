FROM python:3.8

WORKDIR /app

#COPY requirements.txt .

RUN pip install fastapi uvicorn joblib typing pandas numpy

COPY ./app ./app
#COPY ./app/final_model.p ./app/
#ADD ./app/final_scaler.p ./app/
#ADD ./app/music.db ./app/

#COPY ./final_model.p ./app

CMD ["python", "./app/app.py"]

#EXPOSE 8080

#COPY .
#/app /app

#CMD("uvicorn", "app.app:app", "--host", "127.0.0.1", "--port", "8000")
