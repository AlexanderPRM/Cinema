FROM python:3.10


WORKDIR /opt/ugc_etl

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_etl.sh .
COPY /etl .
COPY /src/core core
COPY /src/db db

RUN chmod +x /opt/ugc_etl/run_etl.sh
ENTRYPOINT [ "/opt/ugc_etl/run_etl.sh" ]