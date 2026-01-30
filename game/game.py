import tkinter as tk
from abc import ABC, abstractmethod


class Coordinates(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @abstractmethod
    def move_left(self, speed: int):
        pass

    @abstractmethod
    def move_right(self, speed: int):
        pass

    @abstractmethod
    def jump(self, force: int):
        pass


class Movement(Coordinates):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False

    def move_left(self, speed=50):
        self.x -= speed

    def move_right(self, speed=50):
        self.x += speed

    def jump(self, force=15):
        if not self.is_jumping:
            self.velocity_y = force
            self.is_jumping = True

    def update_physics(self, ground_level=50):
        if self.is_jumping:
            self.y += self.velocity_y
            self.velocity_y -= self.gravity

            if self.y <= ground_level:
                self.y = ground_level
                self.velocity_y = 0
                self.is_jumping = False


WIDTH = 600
HEIGHT = 400

root = tk.Tk()
root.title("Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

canvas.create_rectangle(0, HEIGHT - 50, WIDTH, HEIGHT, fill="green")

player = Movement(300, 50)
player_size = 100

player_emoji = canvas.create_text(
    player.x, HEIGHT - player.y, text="🧍", font=("Segoe UI Emoji", 30)
)


def update():
    player.update_physics()
    canvas.coords(player_emoji, player.x, HEIGHT - player.y)
    root.after(20, update)


def key_press(event):
    if event.keysym == "Left":
        player.move_left()
    elif event.keysym == "Right":
        player.move_right()
    elif event.keysym == "Up":
        player.jump()


root.bind("<KeyPress>", key_press)

update()
root.mainloop()
