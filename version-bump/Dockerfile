FROM python:3-slim AS builder

WORKDIR /app
RUN pip3 install --no-cache-dir pyyaml --target=.
ADD ./main.py .

FROM gcr.io/distroless/python3-debian12

WORKDIR /app
COPY --from=builder /app /app
ENV PYTHONPATH=/app

ENTRYPOINT ["/usr/bin/python3", "-u", "/app/main.py"]
