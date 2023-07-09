FROM python:3.10


WORKDIR /opt/payment_api

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_payment.sh .
COPY /src src
RUN chmod +x /opt/payment_api/run_payment.sh
ENTRYPOINT [ "/opt/payment_api/run_payment.sh" ]