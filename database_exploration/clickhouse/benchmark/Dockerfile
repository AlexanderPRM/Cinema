FROM python:3.10

WORKDIR /opt/bench

RUN apt update && apt-get update && apt-get install python3 -y

COPY requirements.txt .

RUN pip install --upgrade pip \
     && pip install -r requirements.txt
	 
COPY . .

ENTRYPOINT ["sleep", "infinity"]