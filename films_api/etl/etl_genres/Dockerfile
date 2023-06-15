FROM python:3.10

WORKDIR /opt/etl


RUN apt-get update && apt-get install -y \
     python3-dev \
     netcat-openbsd

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /opt/etl/run_etl.sh
ENTRYPOINT [ "/opt/etl/run_etl.sh" ]