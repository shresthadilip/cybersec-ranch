FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{c0rs_m1sc0nf1g_cr3d3nt14l_th3ft_4419}"

CMD ["python", "app.py"]
