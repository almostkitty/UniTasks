FROM python:3.13-slim

WORKDIR /app


RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir git+https://github.com/kurtmckee/feedparser.git

RUN pip install --no-cache-dir Flask==3.0.0 requests==2.31.0 gunicorn==21.2.0 pytest==7.4.3

COPY services/ ./services/

ENV PYTHONUNBUFFERED=1

CMD ["python", "services/news_parser/app.py"]

