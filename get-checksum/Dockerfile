FROM python:3-slim

ADD . /app

WORKDIR /app

RUN pip3 install lxml --target=/app
RUN pip3 install pyyaml --target=/app

ENV PYTHONPATH /app

ENTRYPOINT [ "python", "/app/main.py" ]