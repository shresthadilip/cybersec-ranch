FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{jwt_n0n3_4lg_4nd_w34k_s3cr3t_f0rg3ry}"

CMD ["python", "app.py"]
