from timer_file import Timer
import time

program_timer = Timer()

def main():
    program_timer.start()

    time.sleep(2)

    program_timer.stop()
    print(f"Total time: {program_timer.elapsed():.2f} seconds")

if __name__ == "__main__":
    main()
