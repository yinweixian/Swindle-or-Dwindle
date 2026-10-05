import json
import math
import random

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
        return game_data


    def decrypt_data(self, game_data):
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

    def buy_sell(type, town, player):
        print(f'What resource would you like to {type}?\n\t1. wood\n\t2. diamonds\n\t3. copper\n\t4. lead')
        resource_index = input()
        resource = ''
        match resource_index:
            case '1':
                resource = 'wood'
            case '2':
                resource = 'diamonds'
            case '3':
                resource = 'copper'
            case '4':
                resource = 'lead'
        if resource != '':
            print(f'How many units would you like to {type}?')
            amount = ''
            try:
                amount = int(input())
                if amount < 0:
                    raise ValueError
            except ValueError:
                print("Invalid argument. Transaction incomplete.")
                amount = ''
            if amount != '':
                if type == 'buy':
                    town.buy_from_town(player, resource, amount)
                elif type == 'sell':
                    town.sell_to_town(player, resource, amount)

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
                    buy_sell('buy', town, player)
                case '2':
                    buy_sell('sell', town, player)
                case '3':
                    print(f'Leaving {town.name}.')
                    break
                case 'q':
                    break

    

    game_data = {
        'gold': player.gold,
        'wood': player.resources['wood'],
        'diamonds': player.resources['diamonds'],
        'copper': player.resources['copper'],
        'lead': player.resources['lead'],
    }

    save.write(game_data)

    print(json.dumps(save.read()))

if __name__ == '__main__':
    import sys
    sys.exit(main())