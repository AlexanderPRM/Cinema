FROM python:3.10


WORKDIR /opt/scheduler

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional \
     && rm -rf /var/lib/apt/lists/*

COPY scheduler/requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir


COPY core/ src/core/
COPY providers/ src/providers/
COPY scheduler/run_scheduler.sh .
COPY scheduler .
RUN chmod +x /opt/scheduler/run_scheduler.sh
ENTRYPOINT [ "/opt/scheduler/run_scheduler.sh" ]