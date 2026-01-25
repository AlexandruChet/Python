from abc import ABC, abstractmethod
from datetime import datetime
import json
import uuid
from cryptography.fernet import Fernet


class TrackerStructure(ABC):
    def __init__(self, title, description, target_date, done, id_val):
        self.title = title
        self.description = description
        self.target_date = target_date
        self.done = done
        self.id = id_val

    @abstractmethod
    def save_to_file(self, filename):
        pass

    @abstractmethod
    def task_completed(self):
        pass


class Tracker(TrackerStructure):
    def __init__(self, title="", description="", target_date=None, done=False, id_val=None):
        super().__init__(title, description, target_date, done, id_val or str(uuid.uuid4()))

    def add_habit(self):
        self.title = input("Habit title: ")
        self.description = input("Description: ")

        print("Set your target time:")
        day = int(input("  Day (1-31): "))
        hour = int(input("  Hour (0-23): "))
        minute = int(input("  Minute (0-59): "))

        now = datetime.now()
        self.target_date = datetime(now.year, now.month, day, hour, minute)

    @staticmethod
    def check_deadlines(filename="habits.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                habits = json.load(f)

            now = datetime.now()

            for h in habits:
                if not h["done"] and h["target_date"]:
                        deadline = datetime.strptime(h["target_date"], "%Y-%m-%d %H:%M")
                if now >= deadline:
                        print(f"⏰ Reminder: {h['title']}")

        except FileNotFoundError:
            print("No habits file found.")


    def task_completed(self):
        status = input(f"Did you complete '{self.title}'? (yes/no): ").lower()
        if status == "yes":
            self.done = True
            print("Great job!")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "target_date": self.target_date.strftime("%Y-%m-%d %H:%M") if self.target_date else None,
            "done": self.done
        }

    def save_to_file(self, filename="habits.json"):
        try:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            data.append(self.to_dict())

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"Habit saved to {filename}")
        except Exception as e:
            print(f"Error saving: {e}")

    @staticmethod
    def list_all_habits(filename="habits.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                habits = json.load(f)

            for h in habits:
                status = "✔" if h["done"] else "✘"
                print(f"[{status}] {h['id'][:8]} | {h['title']} (до {h['target_date']})")

        except FileNotFoundError:
            print("No habits found.")

    @staticmethod
    def delete_habit(habit_id, filename="habits.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            data = [h for h in data if h["id"] != habit_id]

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("Habit deleted.")
        except Exception as e:
            print(f"Delete error: {e}")

def values_crypto():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    with open('habits.json', 'r', encoding='utf-8') as f:
        data_file = json.load(f)

    data_str = json.dumps(data_file).encode('utf-8')
    encrypted_data = cipher_suite.encrypt(data_str)

    with open('encrypted_data.bin', 'wb') as f:
        f.write(encrypted_data)

if __name__ == "__main__":
    habit = Tracker()
    habit.add_habit()
    habit.task_completed()
    habit.save_to_file()
    values_crypto()
