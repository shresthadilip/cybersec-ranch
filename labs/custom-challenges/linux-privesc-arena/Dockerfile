FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install SSH, Cron, Sudo, Python3, Text Editors, Tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    cron \
    sudo \
    python3 \
    gcc \
    vim \
    nano \
    curl \
    net-tools \
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setup SSH Server
RUN mkdir -p /run/sshd && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Setup Low-Privilege User: student:student123
RUN useradd -m -d /home/student -s /bin/bash student && \
    echo 'student:student123' | chpasswd && \
    echo 'root:SuperSecretRootPassword992!' | chpasswd

# Flags
RUN echo "CTF{us3r_fl4g_1n1t14l_4cc3ss_5510}" > /home/student/user_flag.txt && \
    chown student:student /home/student/user_flag.txt && \
    chmod 644 /home/student/user_flag.txt

RUN echo "CTF{l1nux_pr1v3sc_gtf0b1ns_m4st3r_7721}" > /root/root_flag.txt && \
    chmod 600 /root/root_flag.txt

# Vector 1: SUID Binary Misconfiguration on /usr/bin/find
RUN chmod u+s /usr/bin/find

# Vector 2: Sudoers Misconfiguration (NOPASSWD for python3)
RUN echo "student ALL=(ALL) NOPASSWD: /usr/bin/python3" >> /etc/sudoers

# Vector 3: World-Writable Root Cron Job
RUN mkdir -p /opt/scripts && \
    printf '#!/bin/bash\n# Scheduled Root Maintenance Script\necho "Running periodic maintenance..." >> /var/log/maintenance.log\n' > /opt/scripts/backup.sh && \
    chmod 777 /opt/scripts/backup.sh && \
    echo "* * * * * root /bin/bash /opt/scripts/backup.sh" > /etc/cron.d/backup_cron && \
    chmod 644 /etc/cron.d/backup_cron

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
