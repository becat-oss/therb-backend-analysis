FROM python:3.9-buster as base

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

CMD ["python","run.py"]