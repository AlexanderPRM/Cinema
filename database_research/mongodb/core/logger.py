import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("mongodb.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
