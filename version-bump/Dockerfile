FROM python:3-slim

ENV PYTHONUNBUFFERED=0

ADD . /app

WORKDIR /app

RUN pip3 install lxml --target=/app
RUN pip3 install pyyaml --target=/app

ENV PYTHONPATH /app

CMD ["/app/main.py"]
ENTRYPOINT [ "python", "-u" ]
