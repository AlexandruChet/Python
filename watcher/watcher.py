import time
from pathlib import Path
import datetime

file = Path("text.txt")

print("Watching for changes")

try:
    last_modified = file.stat().st_mtime

    while True:
        time.sleep(1)

        if not file.exists():
            print("File deleted!")
            break

        current = file.stat().st_mtime
        if current != last_modified:
            last_modified = current
            print("File changed")
            
            modification_time = datetime.datetime.fromtimestamp(current)
            print(f"Last modified time: {modification_time}")

except KeyboardInterrupt:
    print("\nWatcher stopped")
