FROM python:3.10


WORKDIR /opt/admin_api

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional \
     && rm -rf /var/lib/apt/lists/*

COPY admin_api/requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY admin_api/run_admin.sh .
COPY admin_api .
COPY core/ src/core/
RUN chmod +x /opt/admin_api/run_admin.sh
ENTRYPOINT [ "/opt/admin_api/run_admin.sh" ]