FROM python:3.9-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
