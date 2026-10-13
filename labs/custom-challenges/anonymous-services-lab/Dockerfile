FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Samba, Redis, vsftpd
RUN apt-get update && apt-get install -y --no-install-recommends \
    samba \
    smbclient \
    redis-server \
    redis-tools \
    vsftpd \
    net-tools \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ==============================================================================
# 1. Samba (SMB) Anonymous Public Share Setup
# ==============================================================================
RUN mkdir -p /srv/samba/public_share && \
    chmod -R 777 /srv/samba/public_share && \
    printf "Confidential Server Migration Notes\nAuthor: Lead SysAdmin\nFlag: CTF{smb_4n0nym0us_sh4r3_3xfl_8831}\nNote: Please rotate root passwords by end of month.\n" > /srv/samba/public_share/migration_backup_note.txt && \
    printf "Master Server Configuration\nDatabase Host: internal-db.corp.local\nAdmin Port: 9001\n" > /srv/samba/public_share/server_specs.txt && \
    printf "[global]\n   workgroup = WORKGROUP\n   server string = Corporate File Server\n   security = user\n   map to guest = Bad User\n   log file = /var/log/samba/%%m.log\n   max log size = 50\n   dns proxy = no\n\n[public]\n   path = /srv/samba/public_share\n   browsable = yes\n   writable = yes\n   guest ok = yes\n   read only = no\n   create mask = 0777\n   directory mask = 0777\n" > /etc/samba/smb.conf

# ==============================================================================
# 2. Anonymous FTP Configuration (vsftpd)
# ==============================================================================
RUN mkdir -p /srv/ftp/confidential && \
    printf "ACME Corp Internal Financial Report 2026\nQuarterly Revenue: $14.2M\nSecret Audit Flag: CTF{ftp_4n0n_d0wnl04d_pwn3d_1102}\n" > /srv/ftp/confidential/annual_audit.txt && \
    chown -R ftp:ftp /srv/ftp && \
    chmod -R 755 /srv/ftp && \
    mkdir -p /var/run/vsftpd/empty && \
    printf "listen=YES\nlisten_ipv6=NO\nanonymous_enable=YES\nlocal_enable=NO\nwrite_enable=NO\nanon_root=/srv/ftp\nno_anon_password=YES\nftpd_banner=Welcome to ACME Public Storage FTP\nsecure_chroot_dir=/var/run/vsftpd/empty\npam_service_name=vsftpd\n" > /etc/vsftpd.conf

# ==============================================================================
# 3. Redis Setup
# ==============================================================================
RUN sed -i 's/bind 127.0.0.1/bind 0.0.0.0/' /etc/redis/redis.conf && \
    sed -i 's/protected-mode yes/protected-mode no/' /etc/redis/redis.conf

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 445 139 6379 21

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
