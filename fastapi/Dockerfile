FROM python:3.10

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt --verbose

COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

#CMD ["wait-for-it.sh", "db", "--", "uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000"]