FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn

COPY app.py .

EXPOSE 5000

ENV FLAG="CTF{r4c3_c0nd1t10n_t0ct0u_mult1thr34d_pwn3d_7719}"

CMD ["gunicorn", "-w", "1", "--threads", "25", "-b", "0.0.0.0:5000", "app:app"]
