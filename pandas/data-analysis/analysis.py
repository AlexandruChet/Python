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

df = pd.DataFrame(
    [
        {
            "name": u.name,
            "email": u.email,
            "registration_date": u.registration_date,
            "height": u.height,
            "weight": u.weight,
            "age": u.age(),
            "theme": u.preferences.get("theme", "default"),
        }
        for u in users
    ]
)

plt.style.use("seaborn-v0_8")

plt.figure(figsize=(10, 6))
bars = plt.bar(df["name"], df["height"], color="#4A90E2")

plt.title("User Height Comparison", fontsize=16)
plt.xlabel("User", fontsize=12)
plt.ylabel("Height (cm)", fontsize=12)

plt.grid(axis="y", linestyle="--", alpha=0.7)

for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, y + 1, f"{y:.0f}",
             ha="center", fontsize=10)

plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
bars = plt.bar(df["name"], df["weight"], color="#7ED321")

plt.title("User Weight Comparison", fontsize=16)
plt.xlabel("User", fontsize=12)
plt.ylabel("Weight (kg)", fontsize=12)

plt.grid(axis="y", linestyle="--", alpha=0.7)

for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, y + 1, f"{y:.0f}",
             ha="center", fontsize=10)

plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))

plt.hist(df["age"], bins=6, color="#F5A623", edgecolor="black")

plt.title("Age Distribution of Users", fontsize=16)
plt.xlabel("Age")
plt.ylabel("Number of Users")

plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()