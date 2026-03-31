import keyboard
import time

Message = "Hello"
COUNT = 10
DELAY = 0.001

print("Press 'Enter' to START!")
keyboard.wait("enter")
time.sleep(0.5)

for i in range(COUNT):
    if keyboard.is_pressed("esc"):
        break

    keyboard.write(f"{Message}\n")
    time.sleep(DELAY)
