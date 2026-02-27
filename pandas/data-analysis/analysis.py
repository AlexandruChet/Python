from dataclasses import dataclass
from datetime import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

@dataclass
class User:
    name: str
    email: str
    registration_date: str
    preferences: dict
    height: float
    weight: float
    birth_date: str

    def is_one_year_passed(self):
        reg_date = datetime.strptime(self.registration_date, "%Y-%m-%d")
        return (datetime.today() - reg_date).days >= 365

    def age(self):
        bdate = datetime.strptime(self.birth_date, "%Y-%m-%d")
        return (datetime.today() - bdate).days // 365

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

users = [User(**u) for u in data]

df = pd.DataFrame([{
    "name": u.name,
    "email": u.email,
    "registration_date": u.registration_date,
    "height": u.height,
    "weight": u.weight,
    "age": u.age(),
    "theme": u.preferences.get("theme", "default")
} for u in users])

plt.figure(figsize=(8,5))
plt.bar(df['name'], df['height'], color='skyblue')
plt.title("Height of Users")
plt.xlabel("Name")
plt.ylabel("Height (cm)")
plt.show()

plt.figure(figsize=(8,5))
plt.bar(df['name'], df['weight'], color='lightgreen')
plt.title("Weight of Users")
plt.xlabel("Name")
plt.ylabel("Weight (kg)")
plt.show()

plt.figure(figsize=(8,5))
plt.hist(df['age'], bins=5, color='orange', edgecolor='black')
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Users")
plt.show()