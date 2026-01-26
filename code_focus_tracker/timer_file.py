import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.paused_time = 0.0

    def start(self):
        if self.start_time is None:
            self.start_time = time.perf_counter()

    def stop(self):
        if self.start_time is not None:
            self.paused_time += time.perf_counter() - self.start_time
            self.start_time = None

    def reset(self):
        self.start_time = None
        self.paused_time = 0.0

    def elapsed(self):
        if self.start_time:
            return self.paused_time + (time.perf_counter() - self.start_time)
        return self.paused_time
