FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{h4sh_cr4ck1ng_m4st3r_j0hn_h4shc4t_8832}"

CMD ["python", "app.py"]
