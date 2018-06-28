import pygame
from Actors.Actor import Actor
from Actors.Mage import Mage
from Actors.Warrior import Warrior
from Actors.Archer import Archer
from Actors.Faction import Faction
from _thread import start_new_thread
from random import uniform


def main():
    factions = []
    factions.append(Faction("Good guys"))
    factions[0].interactions.append(["Baddies", -10.0])
    factions.append(Faction("Baddies"))
    factions[1].interactions.append(["Good guys", -10.0])

    # hero = Mage(20, 20, "", True)
    # hero.factions.append(factions[0])
    # enemy1 = Archer(1000, 100, "Enemy 1")
    # enemy1.factions.append(factions[1])
    # enemy2 = Warrior(500, 400, "Enemy 2")
    # enemy2.factions.append(factions[1])

    for i in range(10):
        rand = uniform(0,1)
        heroX = int(uniform(0, 1116))
        heroY = int(uniform(0, 444))
        hName = "Hero " + str(i)
        if rand < 0.3333:
            hero = Mage(heroX, heroY, hName)
        elif rand < 0.6666:
            hero = Archer(heroX, heroY, hName)
        else:
            hero = Warrior(heroX, heroY, hName)
        hero.factions.append(factions[0])

        rand = uniform(0,1)
        enemyX = int(uniform(0, 1116))
        enemyY = int(uniform(0, 444))
        eName = "Enemy " + str(i)
        if rand < 0.3333:
            enemy = Mage(enemyX, enemyY, eName)
        elif rand < 0.6666:
            enemy = Archer(enemyX, enemyY, eName)
        else:
            enemy = Warrior(enemyX, enemyY, eName)
        enemy.factions.append(factions[1])


    pygame.init()
    screen = pygame.display.set_mode((1116, 444))


    clock = pygame.time.Clock()
    running = True
    # This loop implements different actions based on the fuzzy logic
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        for actor in Actor.actors_list:
            if actor.is_dead():
                Actor.actors_list.remove(actor)
                continue

            if actor.frame_count == 0:
                start_new_thread(actor.act, ())
            else:
                actor.frame_count -= 1

        screen.fill((0, 0, 0))

        for actor in Actor.actors_list:
            actor.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    if enemy1.hit_points <= 0:
        print("The enemy is dead!")
    else:
        print("You have died!")
    exit()

main()
