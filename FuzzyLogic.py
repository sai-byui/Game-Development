import pygame
from Actors.Actor import Actor
from Actors.Mage import Mage
from Actors.Warrior import Warrior
from Actors.Archer import Archer
from Actors.Faction import Faction


def main():
    factions = []
    factions.append(Faction("Good guys"))
    factions[0].interactions.append(["Baddies", -10.0])
    factions.append(Faction("Baddies"))
    factions[1].interactions.append(["Good guys", -10.0])

    hero = Mage(20, 20, "", True)
    hero.factions.append(factions[0])
    enemy1 = Archer(1000, 100, "Enemy 1")
    enemy1.factions.append(factions[1])
    enemy2 = Warrior(500, 400, "Enemy 2")
    enemy2.factions.append(factions[1])

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
                continue

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
