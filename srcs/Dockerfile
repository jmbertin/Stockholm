FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install cryptography

COPY stockholm.py ./stockholm.py

CMD ["tail", "-f", "/dev/null"]
