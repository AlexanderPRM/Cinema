FROM python:3.10

WORKDIR /opt/auth_api

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_api.sh .
COPY migrations migrations/
COPY src .
COPY openapi.yaml .

RUN chmod +x /opt/auth_api/run_api.sh
ENTRYPOINT [ "/opt/auth_api/run_api.sh" ]