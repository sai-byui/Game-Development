from Actors.Actor import Actor
from Actors.Behavior import Behavior
import random


class Mage(Actor):
    def __init__(self, x, y, name="", player=False):
        super(Mage, self).__init__(x, y, name, player)
        self.max_mana = 100
        self.mana = 100
        self.magic_load = 1.0

    def attempt_attack_behavior(self, current_action):
        if self.healthy > 0.4:
            if self.mana >= 20:
                if self.get_distance_to_object(self.current_target) > 50:
                    approach_action = self.attempt_approach_action(None, 50)
                    if approach_action is not None:
                        current_action = Behavior("Magic Attack!")
                        current_action.is_bottom_level = False
                        current_action.sub_behaviors.append(approach_action)
                        current_action.sub_behaviors.append(
                            Behavior("Magic attack!", self.magic_attack, [self.current_target])
                        )
                else:
                    current_action = Behavior("Magic attack!", self.magic_attack, [self.current_target])
            else:
                if self.get_distance_to_object(self.current_target) > 10:
                    approach_action = self.attempt_approach_action(None, 10)
                    if approach_action is not None:
                        current_action = Behavior("Attack!")
                        current_action.is_bottom_level = False
                        current_action.sub_behaviors.append(approach_action)
                        current_action.sub_behaviors.append(
                            Behavior("Attack!", self.physical_attack, [self.current_target])
                        )
                else:
                    current_action = Behavior("Attack!", self.physical_attack, [self.current_target])
        return current_action

    def magic_attack(self, params):
        print(self.name + " is attacking with magic!")
        if random.uniform(self.accuracy, 1) > random.uniform(params[0].armor_class, 1):
            params[0].take_damage(self.get_magical_damage() - params[0].damage_reduction)
            self.mana -= 20
            self.set_magic_load()
        else:
            print(self.name + " missed!")
        self.frame_count = self.attack_speed
        return True

    def physical_attack(self, params):
        print(self.name + " is Slapping with hand!")
        if random.uniform(self.accuracy, 1) > random.uniform(params[0].armor_class, 1):
            params[0].take_damage(self.get_physical_damage() - params[0].damage_reduction)
        else:
            print(self.name + " missed!")
        self.frame_count = self.attack_speed
        return True

    def set_magic_load(self):
        self.magic_load = float(self.mana) / float(self.max_mana)
