FROM python:3.10


WORKDIR /opt/worker

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional

COPY worker/requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY core/ src/core/
COPY providers/ src/providers/
COPY worker .