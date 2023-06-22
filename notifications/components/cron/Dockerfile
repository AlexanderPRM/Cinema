FROM python:3.10

WORKDIR /opt/cron

RUN apt-get update && apt-get install -y \
     python3-dev   \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_cron.sh .
COPY . .

RUN chmod +x /opt/cron/run_cron.sh
ENTRYPOINT [ "/opt/cron/run_cron.sh" ]