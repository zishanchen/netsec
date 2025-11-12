FROM debian:bookworm
RUN apt update
RUN apt install -y python3 python3-pip netcat-openbsd libpcap0.8
COPY requirements.txt /root/requirements.txt
# COPY prevent_imports.py /root/prevent_imports.py (autograder only)
# COPY restricted_modules.json /root/restricted_modules.json (autograder only)
RUN pip3 install -r /root/requirements.txt --break-system-packages
RUN mkdir /root/hacking
WORKDIR /root/hacking
# Omitted: Autograder forbidden import prevention