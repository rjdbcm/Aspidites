FROM python:3.9.5-slim-buster AS base

RUN apt-get update && apt-get install -y gcc linux-libc-dev python3-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

FROM base AS pyenv
WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .

RUN pip install -U pip && pip install . && pip uninstall -y pip

FROM base AS runtime
## so the test-suite can be run simply using -pt or --pytest
ENV ASPIDITES_DOCKER_BUILD=True
ENV VIRTUAL_ENV=/opt/venv
WORKDIR $VIRTUAL_ENV/lib/python3.9/site-packages/Aspidites/tests
COPY --from=pyenv $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN ln -sf $VIRTUAL_ENV/lib/python3.9/site-packages/Aspidites/tests /workdir
COPY README.md /usr/src/app
ENTRYPOINT ["aspidites"]