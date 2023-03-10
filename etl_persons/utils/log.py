import logging

format = "%(asctime)s - %(name)s - %(message)s"


def get_file_handler() -> logging.FileHandler:
    file_handler = logging.FileHandler("main.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(format))
    return file_handler


def get_stream_handler() -> logging.StreamHandler:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(format))
    return stream_handler


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
