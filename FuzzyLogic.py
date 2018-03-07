# import os
import time
# import random


class Actor:
    def __init__(self):
        self.hit_points = 100
        self.magic_load = 1.0
        self.healthy = 1.0
        self.mana = 100
        self.coverage = 0.0
        self.name = ""

    def set_healthy(self, hit_points):
        self.healthy = hit_points * .01

    def set_magic_load(self, mana):
        self.magic_load = mana * .01

    def take_damage(self, amt):
        self.hit_points -= amt
        self.set_healthy(self.hit_points)
        print(self.name + ", You've been hit dude!")


class Player(Actor):
    def __init__(self):
        super(Player, self).__init__()
        self.name = "player"
        pass

    def magic_attack(self, target):
        print(self.name + " is attacking with magic!")
        target.take_damage(10)
        self.mana -= 20
        self.set_magic_load(self.mana)

    def physical_attack(self, target):
        print(self.name + " is Slapping with hand!")
        target.take_damage(15)

    def hide(self):
        print(self.name + " is Running and Hiding")
        self.coverage = 1

    def drink_potion(self):
        self.hit_points += 30
        self.set_healthy(self.hit_points)
        print(self.name + " is Drinking health juice!")

    def return_to_fight(self):
        self.coverage = 0.0
        print(self.name + " is Coming back out to fight!")


class Enemy(Actor):
    def __init__(self):
        super(Enemy, self).__init__()
        self.rage = 0.0  # fuzzy
        self.name = "enemy"

    def special_attack(self, target):
        print(self.name + " is using special attack!")
        target.take_damage(30)
        self.rage = 0.0

    def magic_attack(self, target):
        print(self.name + " is attacking with magic!")
        target.take_damage(10)
        self.mana -= 20
        self.set_magic_load(self.mana)
        self.rage += 0.3

    def physical_attack(self, target):
        target.take_damage(15)
        self.rage += 0.5
        print(self.name + " is Slapping with hand!")


def main():
    hero = Player()
    enemy = Enemy()

    # This loop implements different actions based on the fuzzy logic
    while enemy.hit_points > 0 and hero.hit_points > 0:
        # take action every three seconds
        time.sleep(3)
        # if the hero has good health and magic, do a magic attack
        if hero.healthy > .5 and hero.magic_load > 0:
            hero.magic_attack(enemy)
        # once we run out of magic, do physicalAttack
        elif hero.healthy > 0.5:
            hero.physical_attack(enemy)
        # if we take too much damage, hide
        elif hero.coverage < 1:
            hero.hide()
            # once we have hidden, take potions to heal
        else:
            hero.drink_potion()
            time.sleep(2)
            hero.return_to_fight()

        if hero.coverage == 0.0:
            if enemy.rage >= 1.0:
                enemy.special_attack(hero)
            elif enemy.magic_load > 0.0:
                enemy.magic_attack(hero)
            else:
                enemy.physical_attack(hero)
        else:
            print("Hero is hidden!")

        print("Player HP: " + str(hero.hit_points))
        print("Enemy HP: " + str(enemy.hit_points))
        print()

    if enemy.hit_points <= 0:
        print("The enemy is dead!")
    else:
        print("You have died!")
    exit()

main()
