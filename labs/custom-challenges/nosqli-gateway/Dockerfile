FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{n05ql_1nj3ct10n_m0ng0_0p3r4t0r_pwnd_8812}"

CMD ["python", "app.py"]
