FROM python:3-slim

RUN pip3 install lxml pyyaml --target=/app

ADD ./main.py /app
WORKDIR /app
ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-u"]
CMD ["/app/main.py"]
