FROM python:3.10

WORKDIR /opt/api


COPY requirements.txt .

RUN apt update && apt-get install python3-dev -y

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_api.sh .
COPY src .

RUN apt install -y netcat
RUN chmod +x /opt/api/run_api.sh
ENTRYPOINT [ "/opt/api/run_api.sh" ]