FROM python:3.10-alpine

LABEL key="Gunicorn SIGTERM"

RUN apk update && \
    apk add curl && \
    apk add git

RUN mkdir -p /app \
    && mkdir -p /tmp \
    && mkdir -p /var/log/gunicorn

COPY . /app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade wheel
RUN pip3 install -r /app/requirements.txt

WORKDIR /app/

EXPOSE 8080

ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:8080", "--timeout", "7200", "-w", "6", "-k", "service_b.worker.CustomWorker", "service_b.app:app"]