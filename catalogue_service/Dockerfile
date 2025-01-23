FROM python:3.10-alpine3.19

RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]