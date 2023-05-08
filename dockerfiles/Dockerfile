FROM python:3.10.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY config config/
COPY src src/
COPY pipeline.py .

CMD ["python", "pipeline.py"]
