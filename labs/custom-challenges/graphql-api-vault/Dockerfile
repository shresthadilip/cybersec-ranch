FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{gr4phql_1ntr0sp3ct10n_s3cr3t_sch3m4_8819}"

CMD ["python", "app.py"]
