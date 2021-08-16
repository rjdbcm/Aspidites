FROM python:3.9.5-slim-buster AS base

RUN apt-get update && apt-get install -y gcc --no-install-recommends

FROM base AS pyenv
WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .

RUN pip install -U pip && pip install .
RUN pip install hypothesis && pip install pytest-mock && pip install pytest-xdist
RUN pip uninstall -y pip

CMD rm -rf /root/.cache/pip

FROM base AS runtime
## so the test-suite can be run
WORKDIR /opt/venv/lib/site-packages/aspidites

ENV VIRTUAL_ENV=/opt/venv
COPY --from=pyenv $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENTRYPOINT ["aspidites"]
CMD ["-h"]