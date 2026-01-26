import time

class Timer:
    def __init__(self) -> None:
        self.start_time = None
        self.paused_time = 0.0

    def start(self):
        if self.start_time is None:
            self.start_time = time.time()
        else:
            print("Timer is already running!")

    def stop(self):
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            self.paused_time += elapsed
            self.start_time = None
        else:
            print("Timer is not running!")

    def reset(self):
        self.start_time = None
        self.paused_time = 0.0

    def elapsed(self):
        if self.start_time is not None:
            return self.paused_time + (time.time() - self.start_time)
        return self.paused_time

ProgramTimer = Timer()

if __name__ == "__main__":
    ProgramTimer.start()
    # the work of the entire program
    ProgramTimer.stop()
    print(f"Program finished in {ProgramTimer.elapsed():.4f} seconds")
