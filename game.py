import random

def main():
    start = input("If you want to start the game, type 'start' or '-' to exit: ").strip().lower()

    if start == "-":
        print("Sad to see you go! :)")
        return
    elif start != "start":
        print("Please write a valid command.")
        return

    print("Download...")
    print('If you want to know the score, enter "see".')
    print('If you want to end, enter "close".')

    user_points = 0
    enemy_points = 0

    rules = {
        "stone": "scissors",
        "scissors": "paper",
        "paper": "stone"
    }

    options = list(rules.keys())

    while True:
        enemy_choice = random.choice(options)
        user = input("\nStone, scissors or paper? (see/close): ").strip().lower()

        if user == "close":
            print(f"Final score - You: {user_points}, Opponent: {enemy_points}")
            print("Game over! Come again!")
            break
        elif user == "see":
            print(f"Your points: {user_points}. Opponent's points: {enemy_points}.")
            continue
        elif user not in options:
            print("Invalid input. Please write paper, scissors, or stone.")
            continue

        if user == enemy_choice:
            print(f"Draw! Opponent also chose {enemy_choice}.")
        elif rules[user] == enemy_choice:
            print(f"You win! {user.capitalize()} beats {enemy_choice}.")
            user_points += 1
        else:
            print(f"You lose! {enemy_choice.capitalize()} beats {user}.")
            enemy_points += 1

if __name__ == "__main__":
    main()
