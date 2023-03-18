FROM python:3.10

WORKDIR /opt/etl_persons

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
     python3-dev \
     netcat

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /opt/etl_persons/run_etl.sh
ENTRYPOINT [ "/opt/etl_persons/run_etl.sh" ]