FROM alpine:3.11.3

RUN apk add --no-cache \
    python3 \
    python3-dev \
    curl \
    musl-dev \
    build-base \
    postgresql-dev

RUN ln -s /usr/bin/python3 /usr/bin/python

# install python dependencies using poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ADD pyproject.toml /gfi/
ADD poetry.lock /gfi/
WORKDIR /gfi/
ENV PYTHONPATH=$PYTHONPATH:/gfi
ENV PATH=$PATH:/root/.poetry/bin
RUN poetry install

ADD . /gfi/
