import logging


def init_logger():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    console_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
