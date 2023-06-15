FROM python:3.10

WORKDIR /opt/admin_panel

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY panel_run.sh .
COPY . .

RUN chmod +x /opt/admin_panel/panel_run.sh
ENTRYPOINT [ "/opt/admin_panel/panel_run.sh" ]