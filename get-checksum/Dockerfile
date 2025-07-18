FROM gcr.io/distroless/python3-debian12:nonroot

ADD . /app

WORKDIR /app

ENV PYTHONPATH=/app

ENTRYPOINT [ "python", "/app/main.py" ]