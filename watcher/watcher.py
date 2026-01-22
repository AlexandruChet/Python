import time
from pathlib import Path
import datetime
import difflib

file = Path("text.txt")

def read_content(e):
    return e.read_text(encoding='utf-8').splitlines() if e.exists() else []

print(f"Watching for changes in {file}...")

try:
    last_modified = file.stat().st_mtime
    old_content = read_content(file)

    while True:
        time.sleep(0.5)

        if not file.exists():
            print("File deleted!")
            break

        current = file.stat().st_mtime
        if current != last_modified:
            new_content = read_content(file)
            
            diff = difflib.ndiff(old_content, new_content)
            
            print(f"\nChange detected: {datetime.datetime.fromtimestamp(current)}")
            
            changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
            if changes:
                print("\n".join(changes))
            else:
                print("Metadata changes or empty change")

            last_modified = current
            old_content = new_content

except KeyboardInterrupt:
    print("\nWatcher stopped")
