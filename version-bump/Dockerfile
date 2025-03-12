FROM debian:12-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests -y --no-install-recommends python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel


FROM build AS build-venv
RUN /venv/bin/pip install --disable-pip-version-check --no-cache-dir lxml
RUN /venv/bin/pip install --disable-pip-version-check --no-cache-dir pyyaml 

FROM gcr.io/distroless/python3-debian12:debug-nonroot AS final

USER nonroot

COPY --from=build-venv /venv /venv
# Must chown files since non-root user doesn't have access to /app to write output file
COPY --chown=nonroot:nonroot . /app

WORKDIR /app

ENTRYPOINT ["/venv/bin/python3", "main.py"]