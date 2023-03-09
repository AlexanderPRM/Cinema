import logging
import time
from functools import wraps

logging.basicConfig(level=logging.DEBUG)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            retries = 0
            sleep_time = start_sleep_time
            while True:
                try:
                    conn = func(*args, **kwargs)
                    retries += 1
                    logging.debug(
                        f"Успешное подключение к базе данных (попытка {retries})"
                    )
                    return conn
                except Exception as error:
                    if sleep_time >= border_sleep_time:
                        logging.error(
                            f"Превышено максимальное время ожидания ({border_sleep_time} секунд)"
                        )
                        raise
                    retries += 1
                    logging.warning(
                        f"Ошибка подключения к базе данных (попытка {retries})"
                    )
                    time.sleep(sleep_time)
                    sleep_time = min(
                        start_sleep_time * (factor**retries), border_sleep_time
                    )

        return inner

    return func_wrapper
