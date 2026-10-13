FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{1d0r_b0l4_pr1v1l3g3_3sc4l4t10n_8821}"

CMD ["python", "app.py"]
