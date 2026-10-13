FROM python:3.11-slim

WORKDIR /app

# Install iputils-ping for ping utility
RUN apt-get update && apt-get install -y --no-install-recommends iputils-ping && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{0s_c0mm4nd_1nj3ct10n_p1ng_pwn3d_4421}"

CMD ["python", "app.py"]
