FROM python:3.9-buster as base

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python","run.py","--host=0.0.0.0","--port=8080"]