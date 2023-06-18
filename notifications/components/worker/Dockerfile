FROM python:3.10

WORKDIR /opt/worker

RUN apt-get update && apt-get install -y \
     python3-dev   \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_worker.sh .
COPY . .

RUN chmod +x /opt/worker/run_worker.sh
ENTRYPOINT [ "/opt/worker/run_worker.sh" ]