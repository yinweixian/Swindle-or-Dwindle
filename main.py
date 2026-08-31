import json
import random

class Town:
    def __init__(self):
       wood: int = random.randint(0, 1000)
       diamonds: int = random.randint(0, 1000)
       copper: int = random.randint(0, 1000)
       lead: int = random.randint(0, 1000)

    def buy_wood(amount: int):
        pass

    def buy_diamonds(amount: int):
        pass

    def buy_copper(amount: int):
        pass

    def buy_lead(amount: int):
        pass

def write_save(save_data):
    save_string: str = json.dumps(save_data)

    with open('game.save', 'w') as save_file:
        save_file.write(save_string)

def read_save():
    try:
        with open('game.save', 'r') as save_file:
            save_string = save_file.read()

        save_data = json.loads(save_string)
    except:
        save_data = {
            'playerName': 'player\'s name',
            'level': 1
        }

    return save_data

def main():
    save_data = read_save()

    write_save(save_data)

    save_data = read_save()
    save_data['level'] = 3

    print(json.dumps(read_save()))

if __name__ == '__main__':
    import sys
    sys.exit(main())
