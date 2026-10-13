FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{f1l3_upl04d_lf1_rce_byp4ss_9934}"

CMD ["python", "app.py"]
