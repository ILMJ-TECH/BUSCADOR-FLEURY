FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]