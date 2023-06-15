FROM python:3.10

WORKDIR /opt/tests

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY run_tests.sh .
COPY . .

RUN chmod +x /opt/tests/run_tests.sh
ENTRYPOINT [ "/opt/tests/run_tests.sh" ]