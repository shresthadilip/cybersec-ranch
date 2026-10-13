FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{55t1_j1nj42_rce_pyth0n_s4ndb0x_3sc4p3}"

CMD ["python", "app.py"]
