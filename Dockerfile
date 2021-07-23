FROM python:3.8

WORKDIR /app

RUN pip install fastapi uvicorn typing pandas numpy scikit-learn==0.23.2 lightgbm python-multipart

COPY ./app ./

CMD ["python", "./app.py"]

EXPOSE 8000
