import json
import math
import random
from encryption_algorithm import encrypt, decrypt

class Town:
    def __init__(self):
        self.name: str = random.choice(('Orem', 'Provo', 'American Fork', 'Pleasant Grove', 'Lehi','Salt Lake'))

        self.gold: int = random.randint(0, 1000)

        self.resources = {
            'wood': random.randint(0, 1200),
            'diamonds': random.randint(0, 50),
            'copper': random.randint(0, 500),
            'lead': random.randint(0, 800),
        }


    def __getitem__(self, key: str):
        return {
            'amount': self.resource[key],
            'price': math.ceil((1 / (self.resource[key] + 1)) * self.gold)
        }

    def __str__(self):
        return self.name

    def __iter__(self):
        return ((
            resource,
            amount,
            math.ceil((1 / (amount + 1)) * self.gold),
        ) for resource, amount in self.resources.items())


    def buy_from_town(self, player: Player, resource: str, amount: int) -> None:
        if player.gold < self[resource]['price'] * amount:
            print('You do not have enough gold.')
            return

        if self.resources[resource] < amount:
            print(f'{self.name} does not have enough of that resource.')
            return

        player.resources[resource] += amount
        player.gold -= self[resource]['price'] * amount
        self.resources[resource] -= amount
        self.gold += self[resource]['price'] * amount


    def sell_to_town(self, player: Player, resource: str, amount: int) -> None:
        if self.gold < self[resource]['price'] * amount:
            print(f'{self.name} does not have enough gold.')
            return

        if player.resources[resource] < amount:
            print('You do not have enough of that resource')
            return 

        player.resources[resource] -= amount
        player.gold += self[resource]['price'] * amount
        self.resources[resource] += amount
        self.gold -= self[resource]['price'] * amount


class Player:
    def __init__(self, gold: int = 10, wood: int = 12, diamonds: int = 0, copper: int = 5, lead: int = 8):
        self.gold: int = gold
        self.resources: dict[str, int] = {
            'wood': wood,
            'diamonds': diamonds,
            'copper': copper,
            'lead': lead,
        }


class Save:
    def __init__(self, file_name = 'game.save'):
        self.file_name = file_name


    def encrypt_data(self, game_data):
        keys = ['gold', 'wood', 'diamonds', 'copper', 'lead']
        for key in keys:
            game_data[key] = encrypt(game_data[key])
        return game_data


    def decrypt_data(self, game_data):
        keys = ['gold', 'wood', 'diamonds', 'copper', 'lead']
        for key in keys:
            game_data[key] = decrypt(game_data[key])
        return game_data
        

    def write(self, game_data):
        save_string: str = json.dumps(self.encrypt_data(game_data))

        with open(self.file_name, 'w') as save_file:
            save_file.write(save_string)


    def read(self):
        with open(self.file_name, 'r') as save_file:
            save_string = save_file.read()

        game_data = self.decrypt_data(json.loads(save_string))

        return game_data


def main():
    save: Save = Save()
    try:
        game_data = save.read()
        player = Player(game_data['gold'], game_data['wood'], game_data['diamonds'], game_data['copper'], game_data['lead'])
    except:
        player = Player()


    choice: str = ''

    while choice != 'q':
        town: Town = Town()

        print(f'You are in {town}.')

        for resource, amount, price in town:
            print(f'\t You can buy up to {amount} units of {resource} @ {price}g/unit.')

        choice = ''
        while True:
            print('What would you like to do?\n\t1. buy\n\t2. sell\n\t3. leave town\n\tq. save and quit')
            choice = input()
            match choice:
                case '1':
                    print('What resource would you like to buy?')
                case '2':
                    print('What resource would you like to sell?')
                case '3':
                    break
                case 'q':
                    break

    game_data = {
        'gold': player.gold,
        'wood': player.wood,
        'diamonds': player.diamonds,
        'copper': player.copper,
        'lead': player.lead,
    }

    save.write(game_data)

    print(json.dumps(save.read()))

if __name__ == '__main__':
    import sys
    sys.exit(main())