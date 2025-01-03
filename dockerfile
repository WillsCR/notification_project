FROM python:3.10-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

WORKDIR /app

EXPOSE 8000

ENTRYPOINT [""]
