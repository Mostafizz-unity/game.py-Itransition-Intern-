import random
import hmac
import hashlib
import sys

# gen hmac
def hmac_sha256(key, message):
    return hmac.new(key, message, hashlib.sha256).hexdigest()
# gen in range 0-5
def get_random_index():
    return random.randint(0, 5)
# get hmac+key 
def get_hmac_and_key():
    key = random.randbytes(16)
    value = get_random_index()
    hmac_value = hmac_sha256(key, str(value).encode())
    return hmac_value, key, value

# cal the result
def fair_roll(secret_value, player_input):
    return (secret_value + player_input) % 6
# balance arguments
def diceArgs(args):
    if len(args) < 3:
        raise ValueError("it accepts 3 or more strings, each containing 6 comma-separated integers. E.g., python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3.")
    dice = []
    for arg in args:
        faces = list(map(int, arg.split(",")))
        if len(faces) != 6:
            raise ValueError("Each die must have exactly 6 numbers.")
        dice.append(faces)
    return dice

def display_dice(dice):
    for idx, die in enumerate(dice):
        print(f"{idx} - {','.join(map(str, die))}")

# all start from here
def main():
    # not less than 3
    # if len(sys.argv) < 3:
    #     print("it accepts 3 or more strings, each containing 6 comma-separated integers. E.g., python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3.")
    #     return
    # first move
    try:
        dice = diceArgs(sys.argv[1:])
    except ValueError as e:
        print(f'Error: {e}')
        return
    print("Let's determine who makes the first move.")

    # Computer value(0 or 1)
    turn_hmac, turn_key, turn_value = get_hmac_and_key()
    print(f"I selected a random value in the range 0..1 (HMAC={turn_hmac}).")
    print("Try to guess my selection.")
    guess = input("0 - 0\n1 - 1\nX - exit\n? - help\nYour selection: ").strip()

    # buttons
    if guess.lower() == 'x':
        return
    elif guess.lower() == '?':
        print("Guess 0 or 1 to decide who goes first.")
        guess = input("Your selection: ").strip()

    try:
        player_guess = int(guess)
    except ValueError:
        print("Invalid input. Exiting.")
        return

    print(f"My selection: {turn_value} (KEY={turn_key.hex()}).")
    player_turn = (player_guess == turn_value)

    # move 
    if player_turn:
        print("You go first.")
    else:
        print("I make the first move.")

    display_dice(dice)
    if player_turn:
        player_die_idx = int(input("Choose your die: "))
        computer_die_idx = random.choice([i for i in range(len(dice)) if i != player_die_idx])
    else:
        computer_die_idx = random.randint(0, len(dice) - 1)
        print(f"I choose the {dice[computer_die_idx]} dice.")
        display_dice([d for i, d in enumerate(dice) if i != computer_die_idx])
        player_die_idx = int(input("Choose your die: "))

    player_die = dice[player_die_idx]
    computer_die = dice[computer_die_idx]

    # Computer roll
    print("It's time for my roll.")
    hmac_comp, comp_key, comp_value = get_hmac_and_key()
    print(f"I selected a random value in the range 0..5 (HMAC={hmac_comp}).")
    comp_input = int(input("Add your number modulo 6.\n0 - 0\n1 - 1\n2 - 2\n3 - 3\n4 - 4\n5 - 5\nYour selection: "))
    print(f"My number is {comp_value} (KEY={comp_key.hex()}).")
    comp_final = fair_roll(comp_value, comp_input)
    comp_roll = computer_die[comp_final]
    print(f"My roll result is {comp_roll}.")

    # Player roll
    print("It's time for your roll.")
    hmac_player, player_key, player_value = get_hmac_and_key()
    print(f"I selected a random value in the range 0..5 (HMAC={hmac_player}).")
    player_input = int(input("Add your number modulo 6.\n0 - 0\n1 - 1\n2 - 2\n3 - 3\n4 - 4\n5 - 5\nYour selection: "))
    print(f"My number is {player_value} (KEY={player_key.hex()}).")
    player_final = fair_roll(player_value, player_input)
    player_roll = player_die[player_final]
    print(f"Your roll result is {player_roll}.")

    # Deceision
    if player_roll > comp_roll:
        print(f"You win ({player_roll} > {comp_roll})! 🎉")
    elif comp_roll > player_roll:
        print(f"I win ({comp_roll} > {player_roll}).")
    else:
        print(f"It's a tie ({player_roll} = {comp_roll}).")

if __name__ == "__main__":
    main()


