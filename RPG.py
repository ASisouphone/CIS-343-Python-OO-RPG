import random

class Home(object):
    def __init__(self):
        pass

class Neighborhood(object):
    def __init__(self):
        pass

class NPC(object):
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def valBetween(self, numA, numB):
        return random.randrange(numA, numB+1, 1)


class Persons(NPC):
    def __init__(self):
        super().__init__(self, "Person", 100, -1)

class Zombies(NPC):
    def __init__(self):
        # super().__init__(name="Zombie", hp=50-100, attack=0-10)
        super().__init__(name="Zombie", hp=super().valBetween(50,100), attack=super().valBetween(0,10))

class Vampires(NPC):
    def __init__(self):
        super().__init__(name="Vampire", hp=super().valBetween(100,200), attack=super().valBetween(10,20))

class Ghouls(NPC):
    def __init__(self):
        super().__init__(name="Ghoul", hp=super().valBetween(40,80), attack=super().valBetween(15,30))

class Werewolves(NPC):
    def __init__(self):
        super().__init__(name="Werewolf", hp=200, attack=super().valBetween(0,40))

class Weapon(object):
    def __init__(self):
        pass
# class Player():
#     def __init__(self):

# class Game(object):
#     pass
def main():
    zombie = Zombies()
    print(zombie.name, zombie.hp, zombie.attack)
    vampire = Vampires()
    print(vampire.name, vampire.hp, vampire.attack)
    ghoul = Ghouls()
    print(ghoul.name, ghoul.hp, ghoul.attack)
    werewolf = Werewolves()
    print(werewolf.name, werewolf.hp, werewolf.attack)

if __name__ == "__main__":
    main()
