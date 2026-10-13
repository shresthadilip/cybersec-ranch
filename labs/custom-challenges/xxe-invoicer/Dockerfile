FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask lxml

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{xx3_3xt3rn4l_3nt1ty_xpl01t_9912}"

CMD ["python", "app.py"]
