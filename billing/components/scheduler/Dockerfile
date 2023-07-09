FROM python:3.10


WORKDIR /opt/scheduler

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_scheduler.sh .
COPY /src src
RUN chmod +x /opt/scheduler/run_payment.sh
ENTRYPOINT [ "/opt/scheduler/run_payment.sh" ]