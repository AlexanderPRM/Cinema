FROM python:3.10


WORKDIR /opt/notification_api

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-openbsd

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_api.sh .
COPY . .
RUN chmod +x /opt/notification_api/run_api.sh
ENTRYPOINT [ "/opt/notification_api/run_api.sh" ]