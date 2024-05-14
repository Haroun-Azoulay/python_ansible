FROM debian:bullseye


RUN apt-get update && \
    apt-get install -y \
    python3-pip

WORKDIR /app

COPY requirements.txt /app/

COPY commands /app/commands

COPY utils /app/utils

RUN pip install -r requirements.txt

COPY . .

COPY inventory.yml default.conf.j2 todos.yml /app/

ENTRYPOINT [ "python3", "main.py", "-f", "todos.yml", "-i", "inventory.yml" ]
