# import os
# import time
import random
import pygame
import math


class Actor:

    actors_list = []

    def __init__(self, x, y, player = False):
        self.x = x
        self.y = y
        self.hit_points = 100
        self.magic_load = 1.0
        self.healthy = 1.0
        self.mana = 100
        self.coverage = 0.0
        self.accuracy = random.uniform(0.5, 1)
        self.strength = random.randint(5, 15)
        self.power = random.randint(10, 15)
        self.armor_class = random.uniform(0.5, 1)
        self.damage_reduction = random.randint(0, 3)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.attack_speed = 120
        self.frame_count = 0
        self.name = ""
        if player:
            self.name = input("What is your name?")

        Actor.actors_list.append(self)

    def set_healthy(self, hit_points):
        self.healthy = hit_points * .01

    def set_magic_load(self, mana):
        self.magic_load = mana * .01

    def take_damage(self, amt):
        if amt > 0:
            self.hit_points -= amt
            self.set_healthy(self.hit_points)
            print(self.name + ", you've been hit for " + str(amt) + " damage!")
            print(self.name + " health: " + str(self.hit_points))

    def get_physical_damage(self):
        return random.randint(self.strength - 2, self.strength + 2)

    def get_magical_damage(self):
        return random.randint(self.power - 2, self.power + 2)

    def drink_potion(self):
        self.hit_points += 30
        self.set_healthy(self.hit_points)
        print(self.name + " is Drinking health juice!")

    def get_distance_to_object(self, obj):
        return math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

    def set_x(self, pos):
        self.x = pos
        self.rect.x = pos

    def set_y(self, pos):
        self.y = pos
        self.rect.y = pos

    # def hide(self):
    #     print(self.name + " is Running and Hiding")
    #     self.coverage = 1
    #
    # def return_to_fight(self):
    #     self.coverage = 0.0
    #     print(self.name + " is Coming back out to fight!")

class Mage(Actor):

    def magic_attack(self, target):
        print(self.name + " is attacking with magic!")
        if random.uniform(self.accuracy, 1) > random.uniform(target.armor_class, 1):
            target.take_damage(self.get_magical_damage() - target.damage_reduction)
            self.mana -= 20
            self.set_magic_load(self.mana)
        else:
            print(self.name + " missed!")
        self.frame_count = self.attack_speed

    def physical_attack(self, target):
        print(self.name + " is Slapping with hand!")
        if random.uniform(self.accuracy, 1) > random.uniform(target.armor_class, 1):
            target.take_damage(self.get_physical_damage() - target.damage_reduction)
        else:
            print(self.name + " missed!")
        self.frame_count = self.attack_speed

class Warrior(Actor):
    def __init__(self):
        super(Warrior, self).__init__()
        self.rage = 0.0  # fuzzy

    def physical_attack(self, target):
        print(self.name + " is Slapping with hand!")
        if random.uniform(self.accuracy, 1) > random.uniform(target.armor_class, 1):
            target.take_damage(self.get_physical_damage() - target.damage_reduction)
        else:
            self.rage += 0.3
            print(self.name + " missed!")
        self.frame_count = self.attack_speed

    def special_attack(self, target):
        print(self.name + " is using special attack!")
        if random.uniform(self.accuracy, 1) > random.uniform(target.armor_class, 1):
            target.take_damage(int(self.get_physical_damage() * 1.5 - target.damage_reduction))
        else:
            print(self.name + " missed!")
        self.rage = 0.0

class Archer(Actor):
    def physical_attack(self, target):
        print(self.name + " is Slapping with hand!")
        if random.uniform(self.accuracy, 1) > random.uniform(target.armor_class, 1):
            target.take_damage(self.get_physical_damage() - target.damage_reduction)
        else:
            print(self.name + " missed!")
        self.frame_count = self.attack_speed

def main():
    hero = Mage(20, 20, True)
    enemy1 = Archer(1000, 100)
    enemy2 = Warrior(500, 400)


    pygame.init()
    screen = pygame.display.set_mode((1116, 444))

    clock = pygame.time.Clock()

    # This loop implements different actions based on the fuzzy logic
    while enemy1.hit_points > 0 and hero.hit_points > 0:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        for actor in Actor.actors_list:
            if actor.frame_count == 0:
                actor.act()
            else:
                actor.frame_count -= 1

        # if hero.frame_count == 0:
        #     # if the hero has good health and magic, do a magic attack
        #     if hero.healthy > .5 and hero.magic_load > 0 and hero.get_distance_to_object(enemy1) < 50:
        #         hero.magic_attack(enemy1)
        #     # once we run out of magic, do physicalAttack
        #     elif hero.healthy > 0.5 and hero.get_distance_to_object(enemy1) < 10:
        #         hero.physical_attack(enemy1)
        #     # if we take too much damage, hide
        #     # elif hero.coverage < 1:
        #         # hero.hide()
        #         # once we have hidden, take potions to heal
        #     elif not hero.healthy > 0.5:
        #         hero.drink_potion()
        #         # time.sleep(2)
        #         # hero.return_to_fight()
        #     else:
        #         x_movement = ((enemy1.x - hero.x) / hero.get_distance_to_object(enemy1))  # / 2.0
        #         y_movement = ((enemy1.y - hero.y) / hero.get_distance_to_object(enemy1))  # / 2.0
        #         hero.x += x_movement
        #         hero.y += y_movement
        #         hero.rect.x = int(hero.x)
        #         hero.rect.y = int(hero.y)
        # else:
        #     hero.frame_count -= 1
        #
        # if hero.coverage == 0.0:
        #     if enemy1.rage >= 1.0:
        #         pass  # enemy.special_attack(hero)
        #     elif enemy1.magic_load > 0.0:
        #         pass  # enemy.magic_attack(hero)
        #     else:
        #         pass  # enemy.physical_attack(hero)
        # else:
        #     print("Hero is hidden!")

        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (255, 0, 0), hero.rect)
        pygame.draw.rect(screen, (0, 0, 255), enemy1.rect)
        pygame.display.flip()

        clock.tick(60)

    if enemy1.hit_points <= 0:
        print("The enemy is dead!")
    else:
        print("You have died!")
    exit()

main()
