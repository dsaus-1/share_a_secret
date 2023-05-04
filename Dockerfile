FROM python:3.7-buster

WORKDIR /code

COPY . .

RUN curl -sSL https://install.python-poetry.org | python3.7 -

ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false \
    && poetry install

CMD python manage.py runserver 0.0.0.0:8000