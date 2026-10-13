FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{p1ckl3_d353r14l1z4t10n_rc3_pwn4g3_9941}"

CMD ["python", "app.py"]
