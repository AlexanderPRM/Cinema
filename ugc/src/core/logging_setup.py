import logging

import logstash
from core.config import project_settings

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logstash.LogstashHandler(project_settings.LOGSTASH_HOST, 5044, version=1))
