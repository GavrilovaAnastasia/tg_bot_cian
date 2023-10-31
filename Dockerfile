FROM python:3.10.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY *.py .

ENTRYPOINT ["python", "main.py"]
