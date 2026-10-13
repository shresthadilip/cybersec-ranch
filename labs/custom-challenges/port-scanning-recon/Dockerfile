FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install essential network services and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    nginx \
    vsftpd \
    postfix \
    mailutils \
    bind9 \
    bind9utils \
    net-tools \
    curl \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ==============================================================================
# 1. SSH Service Configuration (Port 22)
# ==============================================================================
RUN mkdir -p /run/sshd && \
    echo 'root:your_secure_password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# ==============================================================================
# 2. HTTP Web Service Configuration (Nginx - Port 80)
# ==============================================================================
RUN mkdir -p /var/www/html && \
    printf '<!DOCTYPE html>\n<html>\n<head><title>Pokhara Internal Portal</title></head>\n<body style="font-family:sans-serif; background:#0f172a; color:#f8fafc; padding:2rem;">\n<h1>⚡ Pokhara Security Lab Portal</h1>\n<p>Service enumeration successful.</p>\n<div style="background:#1e293b; padding:1rem; border-left:4px solid #38bdf8; font-family:monospace; font-size:1.2rem;">Flag for HTTP: POKHARA_HTTP_FLAG</div>\n</body>\n</html>\n' > /var/www/html/index.html

# ==============================================================================
# 3. FTP Service Configuration (vsftpd - Port 21)
# ==============================================================================
RUN useradd -m -d /home/ftp -s /bin/bash ftpuser && \
    echo 'ftpuser:your_secure_ftp_password' | chpasswd && \
    echo "POKHARA_FTP_FLAG" > /home/ftp/flag.txt && \
    chown -R ftpuser:ftpuser /home/ftp && \
    chmod 755 /home/ftp && \
    chmod 644 /home/ftp/flag.txt && \
    mkdir -p /var/run/vsftpd/empty && \
    printf "listen=YES\nlisten_ipv6=NO\nanonymous_enable=NO\nlocal_enable=YES\nwrite_enable=YES\nlocal_umask=022\ndirmessage_enable=YES\nuse_localtime=YES\nxferlog_enable=YES\nconnect_from_port_20=YES\nftpd_banner=Welcome to the Pokhara FTP server. Flag is in /home/ftp/flag.txt\nsecure_chroot_dir=/var/run/vsftpd/empty\npam_service_name=vsftpd\nrsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem\nrsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key\nssl_enable=NO\n" > /etc/vsftpd.conf

# ==============================================================================
# 4. SMTP Service Configuration (Postfix - Port 25)
# ==============================================================================
RUN postconf -e "inet_interfaces = all" && \
    postconf -e "inet_protocols = ipv4" && \
    postconf -e "myhostname = mail.example.com" && \
    postconf -e "mydestination = example.com, mail.example.com, localhost.localdomain, localhost" && \
    postconf -e "smtpd_banner = \$myhostname ESMTP - Flag for SMTP: POKHARA_SMTP_FLAG"

# ==============================================================================
# 5. DNS Service Configuration (BIND9 - Port 53)
# ==============================================================================
RUN printf 'options {\n    directory "/var/cache/bind";\n    recursion yes;\n    allow-query { any; };\n    listen-on { any; };\n    listen-on-v6 { none; };\n};\n' > /etc/bind/named.conf.options && \
    printf 'zone "example.com" {\n    type master;\n    file "/etc/bind/db.example.com";\n};\n\nzone "0.0.127.in-addr.arpa" {\n    type master;\n    file "/etc/bind/db.127";\n};\n' > /etc/bind/named.conf.local && \
    printf '$TTL 86400\n@ IN SOA ns1.example.com. admin.example.com. (\n    2026092401 ; Serial\n    3600       ; Refresh\n    900        ; Retry\n    604800     ; Expire\n    86400 )    ; Negative Cache TTL\n;\n@        IN  NS    ns1.example.com.\nns1      IN  A     127.0.0.1\nwww      IN  A     127.0.0.1\nmail     IN  A     127.0.0.1\nflag.example.com. IN TXT "Flag for DNS: POKHARA_DNS_FLAG"\n' > /etc/bind/db.example.com && \
    printf '$TTL 86400\n@ IN SOA localhost. root.localhost. (\n    1          ; Serial\n    3600       ; Refresh\n    900        ; Retry\n    604800     ; Expire\n    86400 )    ; Negative Cache TTL\n;\n@        IN  NS    localhost.\n1        IN  PTR   localhost.\n' > /etc/bind/db.127

# Setup entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose all 5 challenge service ports
EXPOSE 22 80 21 25 53/tcp 53/udp

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
