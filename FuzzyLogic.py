import os
import time
import random


class Player:
    def __init__(self):
        self.hitPoints = 100
        self.mana = 100

        # Fuzzy set
        self.healthy = 1.0
        self.magicLoad = 1.0
        self.coverage = 0.0

    def setHealthy(self, hitPoints):
        self.healthy = hitPoints * .01

    def setMagicLoad(self, mana):
        self.magicLoad = mana * .01

    def magicAttack(self, enemy):
        enemy.hitPoints -= 10
        self.mana -= 20
        self.setMagicLoad(self.mana)
        print("attacking with magic!")

    def physicalAttack(self, enemy):
        enemy.hitPoints -= 15
        print("Slapping with hand!")

    def hide(self):
        print("Running and Hiding")
        self.coverage = 1

    def drinkPotion(self):
        self.hitPoints += 30
        self.setHealthy(self.hitPoints)
        print("Drinking health juice!")

    def returnToFight(self):
        self.coverage = 0.0
        print("Coming back out to fight!")

    def takeDamage(self, character):
        self.hitPoints -= 25
        self.setHealthy(self.hitPoints)
        print("\nYou've been hit dude!")

hero = Player()
enemy = Player()

# This loop implements different actions based on the fuzzy logic
while enemy.hitPoints > 0:
    # take action every three seconds
    time.sleep(3)
    # if the hero has good health and magic, do a magic attack
    if hero.healthy > .5 and hero.magicLoad > 0:
        hero.magicAttack(enemy)
    # once we run out of magic, do physicalAttack
    elif hero.healthy > 0.5:
        hero.physicalAttack(enemy)
    # if we take too much damage, hide
    elif hero.coverage < 1:
        hero.hide()
        # once we have hidden, take potions to heal
    else:
        hero.drinkPotion()
        time.sleep(2)
        hero.returnToFight()

    hitGenerator = random.random()
    if hitGenerator > .6 and hero.coverage < 1:
        hero.takeDamage(hero)


print("The enemy is dead!")
exit()






