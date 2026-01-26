import time
import functools
import logging

logging.basicConfig(level=logging.INFO)

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.perf_counter()
            logging.info(
                "%s executed in %.4f seconds",
                func.__name__,
                end - start
            )
    return wrapper


@timer
def complex_data_processing(data_size: int) -> str:
    logging.info("Processing %s elements...", data_size)
    time.sleep(1.5)
    return f"Processed {data_size} items"


result = complex_data_processing(5000)
print(result)
