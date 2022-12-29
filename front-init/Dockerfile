FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install requests

EXPOSE 5050

VOLUME ["/storage/data.json"]

ENTRYPOINT main.py