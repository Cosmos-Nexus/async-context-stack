FROM python:3.11 as builder

ENV PATH="/root/.local/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry self update --preview && \
    poetry config virtualenvs.in-project true


COPY pyproject.toml poetry.lock /venv/

WORKDIR /venv/

RUN poetry install

FROM python:3.11

LABEL version="0.1.0"
LABEL author="Chris Lee"
LABEL email="chris@cosmosnexus.co"
LABEL description="Async context manager for nesting async context stacks"

ENV PYTHONPATH=/actxstack PATH=/venv/.venv/bin:/actxstack/bin:/actxstack/scripts:${PATH}
COPY --from=builder /venv /venv

RUN apt update

WORKDIR /actxstack
COPY . /actxstack


ENTRYPOINT [ "bash" ]
