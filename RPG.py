#!/usr/bin/env python3
from observer import Observer
from observable import Observable
from random import randint, uniform
from pprint import pprint
from abc import abstractmethod
import sys

"""
Parent class of all enemy objects.

Author: Alan Sisouphone
"""
class NPC(Observable):
    def __init__(self, name, hp, attack):
        # Name of NPC
        self.name = name

        # Health points of NPC
        self.hp = hp

        # Attack points of NPC
        self.attack = attack

        # Call Observable constructor
        super().__init__()


    def getName(self):
        """
        Retrieves the name of the NPC
        """
        return self.name

    def isAlive(self):
        """
        Finds if the current NPC is alive or not.
        """
        if (self.hp > 0):
            return True
        return False

    def __str__(self):
        """
        Returns the formatted string of the NPC's fields
        """
        return "%s, HP:%d, Attack:%d" % (self.name, self.hp, self.attack)

    @abstractmethod
    def hurt(self, weapon, playerAttack):
        """
        Allows monsters to be hurt by the player.
        weapon: Weapon player hurts the enemy with
        playerAttack: Attack attribute of the player
        """
        pass

    def hit(self, player):
        """
        Damage the player based on the NPC's attack value.
        """
        print("%s did %d damage!" % (self.name, self.attack))
        player.hurt(self.attack)

"""
Friendly NPC object which will heal the player.
"""
class Persons(NPC):
    def __init__(self):
        # Constructor to create Person as NPC object with 100 health and -1 attack
        super().__init__("Person", 100, -1)

    def hurt(self, weapon, playerAttack):
        """
        Persons is not affected by the player's attacks
        weapon: Weapon of the player
        playerAttack: Attack value of the player
        return: Nothing
        """
        return

"""
Basic Zombie enemy NPC object which can attack the player.
"""
class Zombies(NPC):
    def __init__(self):
        # Creates Zombie as NPC object with 50-100 health and 0-10
        # attack points
        super().__init__(name="Zombie", hp=randint(50,100), attack=randint(0,10))

    def hurt(self, weapon, playerAttack):
        """
        Does damage to the zombie. Zombies get hurt by SourStraws by 2x
        weapon: Weapon used by the player
        playerAttack: Attack value of the player
        """

        damage = 0
        # Damages enemy based on their weakness
        if (weapon.getName() == "SourStraws"):
            damage = (weapon.getAttack() * playerAttack)*2
            print ("SourStraws did double damage!")
            self.hp -= damage
        else:
            damage = (weapon.getAttack() * playerAttack)
            self.hp -= damage

        print("Zombie has taken %d!" % (damage))

        # Manages death of enemy
        if (self.hp <= 0):
            print ("Zombie has died and turned into a person!")

            # Notifies the House object of the death
            self.update()
        print()


"""
Vamprie NPC object which can attack the player and be immune to some attacks.
"""
class Vampires(NPC):
    def __init__(self):

        # Constructor to create Vampire as NPC object with 100-200 health and 100-200
        # attack points
        super().__init__(name="Vampire", hp=randint(100,200), attack=randint(10,20))

    def hurt(self, weapon, playerAttack):
        """
        Does damage to the vampire based on the player's weapon and attack
        weapon: Weapon player uses
        playerAttack: Attack value of the player
        """

        damage = 0
        # Is not affected by ChocolateBars
        if (weapon.getName() == "ChocolateBars"):
            print("Vampires was not effected by chocolate bars!")
            self.hp -= damage
        else:
            damage = (weapon.getAttack() * playerAttack)
            self.hp -= damage

        print ("Vampire received %d damage!" % (damage))

        # Manages death of enemy
        if (self.hp <= 0):
            print ("Vampire has died and turned into a person!")

            # Updates House object of Vampire death
            self.update()
        print()

"""
Ghouls NPC object which can absort some of the player's attack stats.
"""
class Ghouls(NPC):
    def __init__(self):
        # Creates Ghoul as a NPC object with 40-80 health and 15-30
        # attack points
        super().__init__(name="Ghoul", hp=randint(40,80), attack=randint(15,30))

    def hurt(self, weapon, playerAttack):
        """
        Does damage to the ghoul based on the player's weapon and attack values
        weapon: Weapon player uses
        playerAttack: Attack value of the player
        """

        damage = 0
        # Ghouls receive 5x attack if hurt by NerdBombs
        if (weapon.getName() == "NerdBombs"):
            damage = (weapon.getAttack() * playerAttack)
            self.hp -= damage
            self.attack = 5 * playerAttack
            print ("NerdBombs make Ghouls stronger!")
        else:
            damage = (weapon.getAttack() * playerAttack)
            self.hp -= damage

        print ("Ghooul recieved %d damage!" % (damage))

        # Manages death of ghoul
        if (self.hp <= 0):
            print ("Ghoul has died and turned into a person!")

            # Notifies the current house a ghoul has died
            self.update()
        print()

"""
Werewolves NPC object which is immune to multiple weapons.
"""
class Werewolves(NPC):
    def __init__(self):
        # Creates werewolf as a NPC object with 200 health and 0-40
        # attack points
        super().__init__(name="Werewolf", hp=200, attack=randint(0,40))

    def hurt(self, weapon, playerAttack):
        """
        Damages the werewolf object based on the weapon and player's attack value
        """

        damage = 0
        # ChocolateBars and SourStraws do not affect Werewolves
        if (weapon.getName() == "ChocolateBars" or weapon.getName() == "SourStraws"):
            print("Werewolves are not affected by ChocolateBars or SourStraws!")
            self.hp -= damage
        else:
            damage = (weapon.getAttack() * playerAttack)
            self.hp -= damage

        print ("Werewolf has received %s damage!" % (damage))

        # Manages the death of a werewolf
        if (self.hp <= 0):
            print("Werewolf has died and turned into a person!")

            # Notifies the house object a werewolf has died
            self.update()
        print()

"""
Home object which contains a 0-10 monsters and observes each of them and is
observed by the Game object.
"""
class Home(Observer, Observable):
    def __init__(self):
        # Create Home as an Observer object
        Observer.__init__(self)

        # Create Home as an Observable object
        Observable.__init__(self)

        # Monsters/NPCs within the house
        self.monsters = []

        # Populates the homes with random monsters
        for i in range(randint(0,10)):
            randNum = randint(1,5)
            if (randNum == 1):
                currMonster = Persons()
            elif (randNum == 2):
                currMonster = Zombies()
            elif (randNum == 3):
                currMonster = Ghouls()
            elif (randNum == 4):
                currMonster = Vampires()
            elif (randNum == 5):
                currMonster = Werewolves()

            # Has house observe each monster
            currMonster.add_observer(self)
            self.monsters.append(currMonster)

    def updateObserver(self, object):
        """
        Removes a monster from the home if the home is notified.
        object: The monster to be removed
        """
        self.monsters.remove(object)

        # Monsters become persons when they die
        self.monsters.append(Persons())

        # Notifies game the number of monsters has changed
        self.update()

    def getMonsters(self):
        """
        Display the monsters and their stats within the house
        return: A string of the monsters
        """
        tStr = ""
        for monster in self.monsters:
            tStr += monster.__str__() + "\n"
        return tStr

    def getMonsterCount(self):
        """
        Counts the monsters within the house
        return: The number of monters counted
        """
        monCount = 0
        for NPC in self.monsters:
            if (NPC.getName() != "Person"):
                monCount += 1
        return monCount

    def attackAll(self, weapon, playerAttack):
        """
        Hurts all the enemies in the house
        weapon: Weapon item player uses
        playerAttack: Player attack value
        """
        for NPC in self.monsters:
            NPC.hurt(weapon, playerAttack)

    def attackPlayer(self, player):
        """
        Has every monster in the house hurt the player
        """
        for NPC in self.monsters:
            NPC.hit(player)


"""
A grid of houses to represent a neighborhood.
"""
class Neighborhood(object):
    def __init__(self, width, height):

        # Width of the neghborhood
        self.width = width

        # Height of the neighborhood
        self.height = height

        # Creates a grid and populates it with houses randomly
        self.neighborhood = [["O" for x in range(width)] for y in range(height)]
        for i in range(height):
            for j in range(width):
                randNum = randint(0,1)
                if (randNum == 1):
                    self.neighborhood[i][j] = Home()

        # Player starts at 0,0
        self.neighborhood[0][0] = "O"

    def getWidth(self):
        """
        Retrieves the width of the neighborhood
        return: The width
        """
        return self.width

    def getHeight(self):
        """
        Retreives the height of the neighborhood
        return: The height
        """
        return self.height

    def getLayout(self):
        """
        Builds list representation of neighborhood
        returns: List representating the neighborhood
        """

        tList = [["O" for x in range(self.width)] for y in range(self.height)]

        for i in range(self.height):
            for j in range(self.width):
                if (isinstance(self.neighborhood[i][j], Home)):

                    # Houses are represented as H
                    tList[i][j]="H"
        return tList


    def getMonsterCount(self):
        """
        Gets the count of the monsters within each house
        return: Count of all monsters in the neighborhood
        """
        count = 0;
        for row in self.neighborhood:
            for i in row:
                if isinstance(i, Home):
                    count = count + i.getMonsterCount()
        return count

    def getMonstersAt(self, x, y):
        """
        Finds what monsters are at a specific house
        x: x location of monster
        y: y location of monster
        return: A string of monsters
        """
        return self.neighborhood[x][y].getMonsters()

    def isHouse(self, x, y):
        """
        Sees if there is a house at a given position
        x: x location of house
        y: y location of house
        return: True if there is a house
        """

        if (isinstance(self.neighborhood[x][y], Home)):
            return True
        return False

    def houseAt(self, x, y):
        """
        Finds a house at a specific location
        x: x location of house
        y: y location of house
        return: House object
        """
        return self.neighborhood[x][y]

    def gameObserveHouses(self, game):
        """
        Makes each house in neighborhood observed by the game
        game: The game object observing the houses
        """
        for row in self.neighborhood:
            for i in row:
                if isinstance(i, Home):
                    i.add_observer(game)

"""
Parent weapon object to create multiple weapons for the player to attack with.
"""
class Weapon(object):
    def __init__(self, name, attackModif, uses):
        # Name of weapon
        self.name = name

        # Attack modifier to multiply player's attack
        self.attackModif = attackModif

        # Number of uses of weapon
        self.uses = uses

    def getName(self):
        """
        Gets the name of weapon
        return: Weapon name
        """
        return self.name;

    def getAttack(self):
        """
        Gets the attack value of weapon
        return: Attack value
        """
        return self.attackModif

    def getUses(self):
        """
        Gets the number of uses of weapon
        return: The weapon usage
        """
        return self.uses

    def decrUses(self):
        """
        Decriments the number of uses of weapon
        """
        self.uses -= 1

    def __str__(self):
        """
        Creates string format for weapon attributes
        return String format of weapon object
        """
        return "%s, AttackModif: %s, Uses: %s\n" % (self.name, self.attackModif, self.uses)

"""
HersheyKisses uses are infinite but they do one damage
"""
class HersheyKisses(Weapon):
    def __init__(self):
        # Creates HersheyKisses as a weapon object
        super().__init__("HersheyKisses", 1, -1)

"""
SourStraws have a damage modifier from 1-1.75 and has 2 uses
"""
class SourStraws(Weapon):
    def __init__(self):
        # Creates SourStraws as a weapon object
        super().__init__("SourStraws", round(uniform(1.00,1.75),2), 2)

"""
ChocolateBars have a damage modifier from 2-2.40 and has 4 uses
"""
class ChocolateBars(Weapon):
    def __init__(self):
        # Creates ChocolateBars as a weapon object
        super().__init__("ChocolateBars", round(uniform(2.00,2.40),2), 4)

"""
Nerd bombs are the strongest weapon with a modifer of 3.50-5.00 but has 1 use
"""
class NerdBombs(Weapon):
    def __init__(self):
        # Creates NerdBombs as a weapon object
        super().__init__("NerdBombs", round(uniform(3.50, 5.00),2), 1)

"""
Player class which can navigate within a neighborhood and attack monsters within
houses based on its weapon choice and attack stats.
"""
class Player(object):
    def __init__(self):
        # The health points
        self.hp = randint(100,125)

        # Attack stats
        self.attack = randint(10,20)

        # The inventory
        self.weapons = []

        # Current position within neighbhohood
        self.position = {'x':0, 'y':0}

        # Populates player's inventory with random items
        for i in range(10):
            randNum = randint(1,4)
            if (randNum == 1):
                currWeapon = HersheyKisses()
            elif (randNum == 2):
                currWeapon = SourStraws()
            elif (randNum == 3):
                currWeapon = ChocolateBars()
            elif (randNum == 4):
                currWeapon = NerdBombs()
            self.weapons.append(currWeapon)

    def getWeapons(self):
        """
        Helps display the weapons the player has
        return: String of weapons
        """
        weaps = ""
        count = 0
        for weapon in self.weapons:
            weaps+= str(count) + " " + weapon.__str__()
            count += 1
        return weaps

    def getHealth(self):
        """
        Gets the health of the player
        return: Player health
        """
        return self.hp

    def getStats(self):
        """
        Gets the healh and attack stats of the player
        return: Health and attack values
        """
        return "HP:%d, Attack:%d"%(self.hp, self.attack)

    def getPos(self):
        """
        Gets the current position of the player within the neighborhood
        return: Dictionary of player's position
        """
        return self.position

    def move(self, direction):
        """
        Moves player a certain direction
        """
        if (direction == 'W'):
            self.position['x']= self.position['x']-1
        elif(direction == 'S'):
            self.position['x']= self.position['x']+1
        elif(direction == 'A'):
            self.position['y']= self.position['y']-1
        elif(direction == 'D'):
            self.position['y']= self.position['y']+1

    def getWeaponFromNum(self, weapNum):
        """
        Finds the name of a weapon based on its name
        weapNum: The number associated with a weapon
        """
        return self.weapons[weapNum].getName()

    def attackHouse(self, weapNum, house):
        """
        Allows player to attack a house of monsters with a weapon
        weapNum: Number of the weapon chosenWeapon
        house: House the player is attacking
        """
        tWeapon = self.weapons[weapNum]

        if (tWeapon.getUses() != 0):
            tWeapon.decrUses()
            house.attackAll(tWeapon, self.attack)
        else:
            print("GAME: Uses is zero")

    def hurt(self, damage):
        """
        Damages the player based on monster attack
        damage: damage done by monster
        """
        self.hp -= damage

    def isAlive(self):
        """
        Determines whether the player is alive
        return True if palyer is alive
        """
        if (self.hp <= 0):
            return False
        return True

"""
Game object which interacts with all of other objects to create a functional
RPG game. Observes the houses to update current population of monsters.
"""
class Game(Observer):
    def __init__(self, width, height):

        # Player within the game
        self.player = Player()

        # Neighborhood of houses
        self.neighborhood = Neighborhood(width, height)

        # The count of all alive monsters
        self.population = self.neighborhood.getMonsterCount()

        # Allow Game to observe houses
        self.neighborhood.gameObserveHouses(self)

    def updateObserver(self, num):
        """
        Updates population of monsters in the game
        num: Number of monsters removed
        """
        self.population -= 1

    def stats (self):
        """
        Finds stats of the player
        return: Player stats information
        """
        return self.player.getStats()

    def movePlayer(self, direction):
        """
        Moves the player a certain direction on the grid
        """
        self.player.move(direction)

    def getPopulation(self):
        """
        Gets the population of monsters of game
        return: Number of monsters remaining
        """
        return self.population

    def monsterList(self):
        """
        Gets the monsters at the player's current location
        return: List of monsters
        """
        return self.neighborhood.getMonstersAt(self.player.getPos()['x'],self.player.getPos()['y'])

    def weaponsList(self):
        """
        Gets the inventory of the player
        return: List of weapons
        """
        return self.player.getWeapons()

    def hasWon(self):
        """
        Determines whether the player has won or not
        return: True if the player has won
        """
        if (self.population == 0):
            return True
        return False

    def printNeighborhood(self):
        """
        Creates view for of the neighborhood
        return: List view of neighborhood
        """
        tPos = self.player.getPos()
        tList = self.neighborhood.getLayout()

        # Player is represented as a P
        tList[tPos['x']][tPos['y']] = "P"

        return tList


    def inHouse(self, postion):
        """
        Determines whether play is in a house or not
        return: True if the player is in house
        """
        if (self.neighborhood.isHouse(postion["x"],postion["y"]) == True):
            return True
        return False


    def playerPos(self):
        """
        Gets the player's current position in neighborhood
        return: Dictionary of player's position
        """
        return self.player.getPos()


    def attackWith(self, weapNum):
        """
        Attacks the current house with a weapon
        """
        tPos = self.player.getPos()

        self.player.attackHouse(int(weapNum), self.neighborhood.houseAt(tPos['x'], tPos['y']))

    def getWeaponFromNum(self, weapNum):
        """
        Gets the weapon name based on its number
        return: weapon's name
        """
        return self.player.getWeaponFromNum(int(weapNum))

    def isHouseCleared(self):
        """
        Determines whether there are remaining monsters or not
        return: True if the house contains no monsters
        """
        tPos = self.player.getPos()

        if (self.neighborhood.houseAt(tPos['x'], tPos['y']).getMonsterCount() == 0):
            return True
        return False

    def attackPlayer(self):
        """
        Makes the current house and its monster all attack the player
        """
        tPos = self.player.getPos()
        self.neighborhood.houseAt(tPos['x'],tPos['y']).attackPlayer(self.player)

    def isPlayerDead(self):
        """
        Sees if the player is dead or not
        return True if player is dead
        """
        if (self.player.isAlive() is False):
            return True
        return False

    def getHealth(self):
        """
        Gets the current health of the player
        return: Health points of player
        """
        return self.player.getHealth()


"""
Main method to act as a pseudo GUI from the commandline. Interacts with the
game object and allows for user input.
"""
def main():

    # Intro
    print("Hello and welcome to Zork! All your friends ate bad candy and now they are monsters!"
    + " How unfortunate. Now it's your job to turn them back to normal by throwing candy at them.\n")

    # Error handing for width and height
    while True:

        width = input("Please enter the width of your neighborhood:\n")
        height = input ("Please enter the height of it too:\n")

        try:
            gameWidth = int(width)
            gameHeight = int(height)
        except ValueError:
            print("Not a valid integer")
            continue
        if (gameWidth < 1 or gameHeight < 1):
            print("Please provide a positive input value")
            continue
        else:
            break

    # Create game
    game = Game(gameWidth, gameHeight)

    # Main loop until the player has won
    while (game.hasWon() is False):

        print("================================")

        print("Current Population: ",game.getPopulation())

        print("Your stats are", game.stats())

        print('\n'.join(map(' '.join, game.printNeighborhood())))
        print("To move type one of the WASD movement keys e.g 'W' to move North\n")
        print("Or type 'Quit' to exit the program")

        # Error checking for input direction and quit command
        while (True):
            direction = input("Move:\n")
            if (direction not in ["W","A","S","D","Quit"]):
                print("Not valid input")
                continue
            try:
                game.movePlayer(direction)
            except IndexError:
                continue
            else:
                break

        # Quit program
        if (direction == "Quit"):
            sys.exit()

        # Determine whether the player is in a house
        if (game.inHouse(game.playerPos())):
            print("You have entered a house!")
            print("The house is of full of monsters!\n")

            # Keep fighting until the house is cleared of monsters
            while (game.isHouseCleared() == False):
                print("Current Population: ",game.getPopulation())
                print("Current Health:", game.getHealth())
                print("Monsters:\n" + game.monsterList())
                print("What weapon would you like to attack with?")
                print(game.weaponsList())

                # Error handling for choosing weapons
                while True:
                    try:
                        chosenWeapon = int(input("Your Weapon:\n"))
                    except ValueError:
                        print("Not a valid integer")
                        continue
                    if (int(chosenWeapon) < 0 or int(chosenWeapon) > 9):
                        print ("Value not between 0-9")
                        continue
                    else:
                        break

                print("================================")
                print("You chose", game.getWeaponFromNum(chosenWeapon) + "\n")
                print("Now throwing %s mercilessly at the monsters!" % game.getWeaponFromNum(chosenWeapon) + "\n")
                # Player attacks all the enemies
                game.attackWith(chosenWeapon)
                # All the enemies attack the player
                game.attackPlayer()

                # Game Over if the player is dead
                if (game.isPlayerDead() is True):
                    print("Player has died. Game Over")
                    sys.exit()
                print("================================")
            print("You have cleared the house!")

    # Player wins when the player kills all the monsters
    print("Congratulations!! You saved everyone!")

if __name__ == "__main__":
    main()
