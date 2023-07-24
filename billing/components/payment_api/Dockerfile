FROM python:3.10


WORKDIR /opt/payment_api

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional \
     && rm -rf /var/lib/apt/lists/*

COPY payment_api/requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY payment_api/run_payment.sh .
COPY payment_api/ .
COPY core/ src/core/
COPY providers/ src/providers/

RUN chmod +x /opt/payment_api/run_payment.sh
ENTRYPOINT [ "/opt/payment_api/run_payment.sh" ]
