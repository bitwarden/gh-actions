FROM gcr.io/distroless/python3-debian12:nonroot

ADD . /app

WORKDIR /app

RUN pip3 install lxml --target=/app
RUN pip3 install pyyaml --target=/app

ENV PYTHONPATH /app

CMD ["/app/main.py"]
ENTRYPOINT [ "python", "-u" ]
