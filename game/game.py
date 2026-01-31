import tkinter as tk
import time
from abc import ABC, abstractmethod
from enum import Enum

class PlayerState(Enum):
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    ATTACK = "attack"
    DEAD = "dead"

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

    @abstractmethod
    def clamp_position(self, min_x, max_x):
        pass

class Movement(Coordinates):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.state = PlayerState.IDLE
        self.facing = "right"

    def move_left(self, speed=8):
        if self.state != PlayerState.ATTACK:
            self.x -= speed
            self.facing = "left"
            if not self.is_jumping:
                self.state = PlayerState.RUN

    def move_right(self, speed=8):
        if self.state != PlayerState.ATTACK:
            self.x += speed
            self.facing = "right"
            if not self.is_jumping:
                self.state = PlayerState.RUN

    def jump(self, force=15):
        if not self.is_jumping:
            self.velocity_y = force
            self.is_jumping = True
            self.state = PlayerState.JUMP

    def update_physics(self, ground_level=50):
        if self.is_jumping or self.y > ground_level:
            self.y += self.velocity_y
            self.velocity_y -= self.gravity

            if self.y <= ground_level:
                self.y = ground_level
                self.velocity_y = 0
                self.is_jumping = False
                self.state = PlayerState.IDLE

    def clamp_position(self, min_x=20, max_x=580):
        self.x = max(min_x, min(self.x, max_x))

class HeroOptions:
    def __init__(self):
        self.attack_timer = 0
        self.attack_cooldown = 0.5
        self.attack_cd_timer = 0

    def attack(self):
        if self.attack_cd_timer <= 0 and self.state != PlayerState.ATTACK:
            self.state = PlayerState.ATTACK
            self.attack_timer = 0.3
            self.attack_cd_timer = self.attack_cooldown

    def update_attack(self, delta_time):
        if self.state == PlayerState.ATTACK:
            self.attack_timer -= delta_time
            if self.attack_timer <= 0:
                self.state = PlayerState.IDLE

        if self.attack_cd_timer > 0:
            self.attack_cd_timer -= delta_time

class Hero(Movement, HeroOptions):
    def __init__(self, x: int, y: int):
        Movement.__init__(self, x, y)
        HeroOptions.__init__(self)

    def update(self, delta_time):
        self.update_physics()
        self.update_attack(delta_time)
        self.clamp_position()

WIDTH, HEIGHT = 600, 400
GROUND_LEVEL = 50

root = tk.Tk()
root.title("Mini Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#87CEEB", outline="")
canvas.create_rectangle(0, HEIGHT*0.6, WIDTH, HEIGHT, fill="#9be564", outline="")
ground = canvas.create_rectangle(0, HEIGHT - GROUND_LEVEL, WIDTH, HEIGHT, fill="#3b7a57", outline="")

clouds = [canvas.create_oval(x, 40, x+60, 70, fill="white", outline="") for x in (100, 300, 500)]

def move_clouds():
    for cloud in clouds:
        canvas.move(cloud, 0.3, 0)
        if canvas.coords(cloud)[0] > WIDTH:
            canvas.move(cloud, -WIDTH-100, 0)

player = Hero(300, GROUND_LEVEL)

player_shadow = canvas.create_oval(0, 0, 0, 0, fill="#444444", outline="")
player_body = canvas.create_oval(0, 0, 0, 0, fill="#659adf", outline="")
player_weapon = canvas.create_rectangle(0, 0, 0, 0, fill="silver", outline="")

def draw_attack():
    if player.state == PlayerState.ATTACK:
        if player.facing == "right":
            canvas.coords(player_weapon,
                        player.x+15, HEIGHT-player.y-10,
                        player.x+40, HEIGHT-player.y+10)
        else:
            canvas.coords(player_weapon,
                        player.x-40, HEIGHT-player.y-10,
                        player.x-15, HEIGHT-player.y+10)
    else:
        canvas.coords(player_weapon, 0, 0, 0, 0)

keys_pressed = set()

def key_press(event):
    keys_pressed.add(event.keysym)

def key_release(event):
    keys_pressed.discard(event.keysym)

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

def handle_keys():
    if "Left" in keys_pressed:
        player.move_left()
    if "Right" in keys_pressed:
        player.move_right()
    if "Up" in keys_pressed:
        player.jump()
    if "space" in keys_pressed:
        player.attack()

last_time = time.time()

def update():
    global last_time
    now = time.time()
    delta_time = now - last_time
    last_time = now

    handle_keys()
    player.update(delta_time)
    move_clouds()

    canvas.coords(player_shadow,
                player.x-15, HEIGHT-GROUND_LEVEL,
                player.x+15, HEIGHT-GROUND_LEVEL+5)

    canvas.coords(player_body,
                player.x-10, HEIGHT-player.y-30,
                player.x+10, HEIGHT-player.y)

    draw_attack()
    root.after(16, update)

update()
root.mainloop()
