import time
from contextlib import contextmanager

@contextmanager
def timer(task_name):
    print(f"Start: {task_name}")
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"processed in {end - start:.4f} seconds")

with timer("Work with list"):
    data = [x**2 for x in range(10**6)]
    print(f"processed {len(data)} elements")
