import random
import pygame
from Actors.Behavior import Behavior
from util import distance
import time


class Actor:

    actors_list = []

    def __init__(self, x, y, name, player=False):
        self.x = x
        self.y = y
        self.max_hit_points = 100
        self.hit_points = 100
        self.healthy = 1.0
        self.health_potion_remaining = 100
        self.coverage = 0.0
        self.accuracy = random.uniform(0.5, 1)
        self.strength = random.randint(5, 15)
        self.power = random.randint(10, 15)
        self.armor_class = random.uniform(0.5, 1)
        self.damage_reduction = random.randint(0, 3)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.attack_speed = 120
        self.frame_count = 0
        self.current_color = (255, 255, 255)
        self.current_action = None
        self.name = name
        self.frames_since_behavior_decided = 0
        self.current_max_attack_range = 5  # Determined by whether the char can currently make a ranged attack
        self.current_target = None
        self.factions = []
        self.done_acting = True
        if player:
            self.name = input("What is your name?")

        Actor.actors_list.append(self)

    def act(self):
        if self.done_acting:
            self.done_acting = False
            self.frames_since_behavior_decided += 1
            if self.current_action is None or self.frames_since_behavior_decided >= 70:
                self.current_action = self.decide_behavior()
                time.sleep(0.001)
                self.current_color = (255, 255, 255)
            if self.current_action.perform_action(self):
                self.current_action = None
            self.done_acting = True


    def approach(self, params):
        if distance((self.x, self.y), (params[0], params[1])) > params[2]:
            dist = distance((self.x, self.y), (params[0], params[1]))
            x_movement = ((params[0] - self.x) / dist)
            y_movement = ((params[1] - self.y) / dist)
            self.x += x_movement
            self.y += y_movement
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
        else:
            return True
        return False

    def attempt_approach_action(self, current_action, to_within):
        return Behavior("Approach", self.approach, [self.current_target.x, self.current_target.y, to_within])

    def attempt_attack_behavior(self, current_action):
        print("************************************************************************************")
        print("ERROR: method attempt_attack_behavior must be implemented in child classes of Actor.")
        print("************************************************************************************")
        exit(1)

    def attempt_heal_behavior(self, current_action):
        if self.health_potion_remaining > 0:
            if self.healthy < 1.0:
                return Behavior("Heal", self.heal_self)
        return current_action

    def attempt_hide_behavior(self, current_action):  # Implement later, after walls and pathfinding
        return current_action

    def check_for_targets(self):
        self.current_target = None
        for actor in Actor.actors_list:
            if actor == self:
                continue

            if actor.is_dead():
                continue

            if self.current_target is None:
                self.current_target = actor
            elif isinstance(self.current_target, Actor) and self.is_hostile_towards(self.current_target):
                if self.is_hostile_towards(actor) \
                        and self.get_distance_to_object(actor) < self.get_distance_to_object(self.current_target):
                    self.current_target = actor

    def decide_behavior(self):
        self.frames_since_behavior_decided = 0

        self.check_for_targets()

        current_action = Behavior("Do nothing", self.do_nothing)
        current_action = self.attempt_heal_behavior(current_action)
        current_action = self.attempt_hide_behavior(current_action)
        if self.current_target is not None and self.is_hostile_towards(self.current_target):
            current_action = self.attempt_attack_behavior(current_action)
        return current_action

    def do_nothing(self, params):  # Dummy function to use as a callback
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        font = pygame.font.SysFont('Arial', 25)
        screen.blit(font.render(self.name, True, (255, 255, 255)), (self.x, self.y + 20))

    def get_distance_to_object(self, obj):
        return distance((self.x, self.y), (obj.x, obj.y))

    def get_magical_damage(self):
        return random.randint(self.power - 2, self.power + 2)

    def get_physical_damage(self):
        return random.randint(self.strength - 2, self.strength + 2)

    def heal_self(self, params):
        self.current_color = (0, 255, 0)
        amt_to_heal = self.max_hit_points - self.hit_points
        if amt_to_heal > self.health_potion_remaining:
            amt_to_heal = self.health_potion_remaining
        self.hit_points += amt_to_heal
        self.health_potion_remaining -= amt_to_heal
        self.set_healthy()
        print(self.name + " is Drinking health juice!")
        return True

    def is_dead(self):
        return self.healthy <= 0.0

    def is_hostile_towards(self, actor):
        total_standing = 0.0
        num_standings = 0.0
        for self_faction in self.factions:
            for actor_faction in actor.factions:
                for interaction in self_faction.interactions:
                    if interaction[0] == actor_faction.name:
                        total_standing += interaction[1]
                        num_standings += 1
        if num_standings == 0:
            return False
        if total_standing / num_standings < -2.0:
            return True
        return False

    def set_healthy(self):
        self.healthy = float(self.hit_points) / float(self.max_hit_points)

    def set_x(self, pos):
        self.x = pos
        self.rect.x = pos

    def set_y(self, pos):
        self.y = pos
        self.rect.y = pos

    def take_damage(self, amt):
        if amt > 0:
            self.hit_points -= amt
            self.set_healthy()
            print(self.name + ", you've been hit for " + str(amt) + " damage!")
            print(self.name + " health: " + str(self.hit_points))
