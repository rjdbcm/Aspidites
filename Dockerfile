FROM python:3.9.5-alpine3.14 as base

WORKDIR /usr/src/app

RUN apk add build-base
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir Aspidites

ENTRYPOINT ["aspidites"]
CMD ["-h"]