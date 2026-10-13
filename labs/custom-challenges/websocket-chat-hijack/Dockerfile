FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask flask-sock

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{csw5h_w3bs0ck3t_h1j4ck_0r1g1n_pwn_5512}"

CMD ["python", "app.py"]
