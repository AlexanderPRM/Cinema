FROM python:3.10

WORKDIR /opt/etl_persons

COPY requirements.txt .

RUN apt update && apt-get install python3-dev -y

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN apt install -y netcat
RUN chmod +x /opt/etl_persons/run_etl.sh
ENTRYPOINT [ "/opt/etl_persons/run_etl.sh" ]