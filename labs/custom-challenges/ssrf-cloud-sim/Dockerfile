FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{55rf_cl0ud_m3t4d4t4_3xf1ltr4t10n_9921}"

CMD ["python", "app.py"]
