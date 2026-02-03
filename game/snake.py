import tkinter as tk
import random

UNIT_SIZE = 25
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 100


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Python")
        self.canvas = tk.Canvas(self.window, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.canvas.pack()
        self.running = False
        self.score = 0
        self.food_x = 0
        self.food_y = 0
        self.x_velocity = UNIT_SIZE
        self.y_velocity = 0
        self.snake = []
        self.window.bind("<Key>", self.change_direction)
        self.reset_game()

    def create_food(self):
        self.food_x = random.randint(0, (GAME_WIDTH // UNIT_SIZE) - 1) * UNIT_SIZE
        self.food_y = random.randint(0, (GAME_HEIGHT // UNIT_SIZE) - 1) * UNIT_SIZE

    def draw_food(self):
        self.canvas.create_oval(
            self.food_x,
            self.food_y,
            self.food_x + UNIT_SIZE,
            self.food_y + UNIT_SIZE,
            fill="#0c4de7",
            outline="",
            tags="food",
        )
        self.canvas.create_oval(
            self.food_x + 5,
            self.food_y + 5,
            self.food_x + 12,
            self.food_y + 12,
            fill="#9ea8ef",
            outline="",
            tags="food",
        )

    def clear_board(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0, 0, GAME_WIDTH, GAME_HEIGHT, fill="#99aeca", outline=""
        )

    def draw_snake(self):
        for i, part in enumerate(self.snake):
            color = "#083275" if i == 0 else "lightblue"
            self.canvas.create_rectangle(
                part["x"],
                part["y"],
                part["x"] + UNIT_SIZE,
                part["y"] + UNIT_SIZE,
                fill=color,
                outline="#FFFFFF",
                width=2,
            )

    def move_snake(self):
        head = {
            "x": self.snake[0]["x"] + self.x_velocity,
            "y": self.snake[0]["y"] + self.y_velocity,
        }
        self.snake.insert(0, head)

        if head["x"] == self.food_x and head["y"] == self.food_y:
            self.score += 1
            self.create_food()
        else:
            self.snake.pop()

    def next_tick(self):
        if self.running:
            self.clear_board()
            self.draw_food()
            self.move_snake()
            self.draw_snake()
            self.check_game_over()
            self.window.after(SPEED, self.next_tick)
        else:
            self.display_game_over()

    def change_direction(self, event):
        key = event.keysym
        match key:
            case "Left" if self.x_velocity != UNIT_SIZE:
                self.x_velocity, self.y_velocity = -UNIT_SIZE, 0
            case "Up" if self.y_velocity != UNIT_SIZE:
                self.x_velocity, self.y_velocity = 0, -UNIT_SIZE
            case "Right" if self.x_velocity != -UNIT_SIZE:
                self.x_velocity, self.y_velocity = UNIT_SIZE, 0
            case "Down" if self.y_velocity != -UNIT_SIZE:
                self.x_velocity, self.y_velocity = 0, UNIT_SIZE

    def check_game_over(self):
        head = self.snake[0]
        if (
            head["x"] < 0
            or head["x"] >= GAME_WIDTH
            or head["y"] < 0
            or head["y"] >= GAME_HEIGHT
        ):
            self.running = False

        for part in self.snake[1:]:
            if head["x"] == part["x"] and head["y"] == part["y"]:
                self.running = False

    def display_game_over(self):
        self.running = False
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2,
            text="GAME OVER",
            fill="#000000",
            font=("Arial", 40, "bold"),
        )

        self.window.after(1000, self.reset_game)

    def reset_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.x_velocity = UNIT_SIZE
        self.y_velocity = 0
        self.snake = [{"x": UNIT_SIZE * i, "y": 0} for i in range(4, -1, -1)]
        self.running = True
        self.create_food()
        self.next_tick()


if __name__ == "__main__":
    game = SnakeGame()
    game.window.mainloop()
