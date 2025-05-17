FROM python:3.9-slim

WORKDIR /src

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "src"]
