import time
from pathlib import Path

file = Path("text.txt")

print("Watching for changes... (Ctrl+C to stop)")

try:
    last_modified = file.stat().st_mtime

    while True:
        time.sleep(1)

        if not file.exists():
            print("File deleted!")
            break

        current = file.stat().st_mtime
        if current != last_modified:
            print("File changed")
            last_modified = current

except KeyboardInterrupt:
    print("\nWatcher stopped")
