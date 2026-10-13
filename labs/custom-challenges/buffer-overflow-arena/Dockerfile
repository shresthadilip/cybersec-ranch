FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY vuln.c .

# Compile 64-bit binary without stack protector and with fixed addresses (no-pie)
RUN gcc -fno-stack-protector -no-pie -z execstack -Wno-implicit-function-declaration -o vuln vuln.c

ENV FLAG="CTF{buff3r_0v3rfl0w_r3t2w1n_pwn_m4st3r_64b1t_8829}"

RUN echo "$FLAG" > /flag.txt && chmod 644 /flag.txt

EXPOSE 5000

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:/app/vuln"]
