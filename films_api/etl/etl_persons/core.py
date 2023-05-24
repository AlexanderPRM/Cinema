import datetime
import logging
import time

import backoff
import elasticsearch
from etl_process.extract import Extract
from etl_process.load import Load
from etl_process.transform import Transform
from storage import JsonFileStorage, State
from utils.dsn import Config
from utils.log import get_logger


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=elasticsearch.exceptions.ConnectionError,
    max_tries=30,
)
def etl(logger: logging.Logger, extract: Extract, transform: Transform, state: State, load: Load):
    sync = state.get_state("sync")
    logger.info("Last sync: {0}".format(sync))
    start_timestamp = datetime.datetime.now()
    person_ids = state.get_state("stopped_uuid")

    for extracted_part in extract.extract(sync, start_timestamp, person_ids):
        data = transform.transform(extracted_part)
        load.load(data)
        state.set_state("sync", str(start_timestamp))
        state.set_state("stopped_uuid", [])


if __name__ == "__main__":
    config = Config()
    logger = get_logger(__name__)
    state = State(JsonFileStorage(file_path="state.json"))
    extract = Extract(
        psql_dsn=config.dsn, chunk_size=config.batch_size, storage_state=state, logger=logger
    )
    transform = Transform()
    load = Load(dsn=f"http://{config.es_host}:{config.es_port}", logger=logger)
    while True:
        etl(logger, extract, transform, state, load)
        logger.info("Sleep for 60 sec")
        time.sleep(config.etl_timeout)
