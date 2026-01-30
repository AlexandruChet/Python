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

    def move_left(self, speed=5):
        self.x -= speed

    def move_right(self, speed=5):
        self.x += speed

    def jump(self, force=15):
        if not self.is_jumping:
            self.velocity_y = force
            self.is_jumping = True

    def update_physics(self, ground_level=0):
        if self.is_jumping:
            self.y += self.velocity_y
            self.velocity_y -= self.gravity

            if self.y <= ground_level:
                self.y = ground_level
                self.velocity_y = 0
                self.is_jumping = False
