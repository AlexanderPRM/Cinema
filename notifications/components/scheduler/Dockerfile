FROM python:3.10

WORKDIR /opt/scheduler

RUN apt-get update && apt-get install -y \
     python3-dev   \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY entrypoint.sh .
COPY src .

RUN chmod +x /opt/scheduler/entrypoint.sh
ENTRYPOINT [ "/opt/scheduler/entrypoint.sh" ]