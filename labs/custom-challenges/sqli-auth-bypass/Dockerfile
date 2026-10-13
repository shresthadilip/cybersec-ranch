FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{5ql_1nj3ct10n_m4st3r_byp4ss_2026}"

CMD ["python", "app.py"]
