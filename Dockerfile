FROM alpine:3.11.3

RUN apk add --no-cache \
    python3 python3-dev curl musl-dev build-base
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH=$PATH:/root/.poetry/bin

ADD . /app/
WORKDIR /app/
RUN (cd poetry-project && poetry install)

ENTRYPOINT [ "sleep", "infinity" ]
