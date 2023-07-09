FROM python:3.10


WORKDIR /opt/billing_api

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_billing.sh .
COPY /src src
RUN chmod +x /opt/billing_api/run_billing.sh
ENTRYPOINT [ "/opt/billing_api/run_billing.sh" ]