import random
from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, str_val, sp, n, heal, def_val):
        self.strength = str_val
        self.speed = sp
        self.name = n
        self.health = heal
        self.defense_value = def_val
        self.dodging = False

    @abstractmethod
    def attack(self, target: 'Character'):
        pass

    @abstractmethod
    def defense(self):
        pass

    @abstractmethod
    def recovery(self):
        pass

    @abstractmethod
    def miss(self) -> bool:
        pass

    @abstractmethod
    def random_perk(self, target: 'Character'):
        pass

    def take_damage(self, dmg):
        self.health -= dmg

    def add_defense(self, value):
        self.defense_value += value

    def add_strength(self, value):
        self.strength += value

    def heal(self, value):
        self.health += value

    def get_health(self):
        return self.health

    def set_dodging(self, value: bool):
        self.dodging = value

    def is_dodging(self) -> bool:
        return self.dodging


class Hero(Character):
    def __init__(self):
        super().__init__(50, 100, "Hero", 100, 30)
        self.mana = 100

    def attack(self, target: Character):
        if target.is_dodging():
            print("Hero attacks, but enemy dodges!")
            target.set_dodging(False)
            return

        if self.miss():
            print("Hero missed!")
            self.mana -= 10
            return

        dmg = self.strength if random.random() < 0.8 else self.strength * 1.5
        target.take_damage(dmg)
        print(f"Hero deals {dmg} damage!")

    def defense(self):
        self.add_defense(30)

    def recovery(self):
        self.heal(30)

    def miss(self) -> bool:
        return random.randint(0, 99) >= 80

    def use_miss(self):
        if self.mana < 20:
            print("Not enough mana to dodge!")
            return
        self.mana -= 10
        self.set_dodging(True)
        print(f"Hero prepares to dodge! (Mana: {self.mana})")

    def random_perk(self, target: Character):
        perks = ["Defense", "Attack", "Health", "Mana", "", ""]
        perk = random.choice(perks)

        if perk == "Defense":
            target.add_defense(100)
            print("Bonus: Target +100 Defense")
        elif perk == "Attack":
            target.add_strength(50)
            print("Bonus: Target +50 Strength")
        elif perk == "Health":
            target.heal(100)
            print("Bonus: Target +100 Health")
        elif perk == "Mana":
            self.mana += 100
            print("Bonus: Hero +100 Mana")
        else:
            self.take_damage(5)
            print("Bad luck: Hero takes 5 damage")

class Enemy(Character):
    def __init__(self):
        super().__init__(35, 60, "Enemy", 300, 10)
        self.mana = 50

    def attack(self, target: Character):
        if target.is_dodging():
            print("Enemy attacks, but hero dodges!")
            target.set_dodging(False)
            return

        if self.miss():
            print("Enemy missed!")
            return

        dmg = self.strength if random.randint(0, 99) < 80 else self.strength * 1.1
        target.take_damage(dmg)
        print(f"Enemy deals {dmg:.1f} damage!")

    def use_miss(self):
        if self.mana < 10:
            return
        self.mana -= 10
        self.dodging = True
        print("Enemy prepares to dodge!")

    def defense(self):
        self.add_defense(10)
        print("Enemy increases defense!")

    def recovery(self):
        self.heal(15)
        print("Enemy recovers health!")

    def miss(self) -> bool:
        return random.randint(0, 99) >= 80

    def random_perk(self, target: Character):
        random_chance = random.randint(1, 4)
        
        if random_chance == 1:
            self.attack(target)
        elif random_chance == 2:
            self.defense()
        elif random_chance == 3:
            self.recovery()
        elif random_chance == 4:
            self.miss()
        else:
            print("Error")

def battle():
    hero = Hero()
    enemy = Enemy()
    turn = 1

    while hero.get_health() > 0 and enemy.get_health() > 0:
        print(f"\n--- TURN {turn} ---")
        print(f"Hero HP: {hero.health} | Mana: {hero.mana}")
        print(f"Enemy HP: {enemy.health}")

        print("\nChoose action:")
        print("1 - Attack")
        print("2 - Defense")
        print("3 - Recovery")
        print("4 - Dodge")
        print("5 - Random perk")

        choice = input("Your choice: ")

        if choice == "1":
            hero.attack(enemy)
        elif choice == "2":
            hero.defense()
            print("Hero increases defense!")
        elif choice == "3":
            hero.recovery()
            print("Hero recovers health!")
        elif choice == "4":
            hero.use_miss()
        elif choice == "5":
            hero.random_perk(enemy)
        else:
            print("Invalid choice!")
            continue

        if enemy.get_health() > 0:
            print("\nEnemy's turn...")
            action = random.randint(1, 4)

            if action == 1:
                enemy.attack(hero)
            elif action == 2:
                enemy.defense()
            elif action == 3:
                enemy.recovery()
            elif action == 4:
                enemy.use_miss()

        turn += 1

    print("\n=== BATTLE OVER ===")
    print("You won 🎉" if hero.get_health() > 0 else "You lost 😢")

if __name__ == "__main__":
    battle()
