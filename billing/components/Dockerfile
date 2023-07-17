FROM python:3.10


WORKDIR /opt/migrations

RUN apt-get update && apt-get install -y \
     python3-dev

COPY alembic_req.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r alembic_req.txt --no-cache-dir

COPY alembic.ini .
COPY alembic alembic
COPY admin_api/src/db/models.py admin_api/src/db/
COPY payment_api/src/db/models.py payment_api_api/src/db/
COPY billing_api/src/db/models.py billing_api/src/db/
CMD ["alembic", "upgrade", "head"]