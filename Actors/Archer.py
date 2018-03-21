from Actors.Actor import Actor
import random
from Actors.Behavior import Behavior


class Archer(Actor):
    def __init__(self, x, y, name="", player=False):
        super(Archer, self).__init__(x, y, name, player)
        self.num_arrows = 10

    def attempt_attack_behavior(self, current_action):
        if self.healthy > 0.4:
            if self.num_arrows >= 1:
                if self.get_distance_to_object(self.current_target) > 50:
                    approach_action = self.attempt_approach_action(None, 50)
                    if approach_action is not None:
                        current_action = Behavior("Ranged Attack!")
                        current_action.is_bottom_level = False
                        current_action.sub_behaviors.append(approach_action)
                        current_action.sub_behaviors.append(
                            Behavior("Ranged attack!", self.ranged_attack, [self.current_target])
                        )
                else:
                    current_action = Behavior("Ranged attack!", self.ranged_attack, [self.current_target])
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

    def get_ranged_damage(self):
        return self.get_physical_damage()

    def physical_attack(self, params):
        print(self.name + " is Slapping with hand!")
        if random.uniform(self.accuracy, 1) > random.uniform(params[0].armor_class, 1):
            params[0].take_damage(self.get_physical_damage() - params[0].damage_reduction)
        else:
            print(self.name + " missed!")
        self.frame_count = self.attack_speed
        return True

    def ranged_attack(self, params):
        print(self.name + " is shooting with arrow!")
        if random.uniform(self.accuracy, 1) > random.uniform(params[0].armor_class, 1):
            params[0].take_damage(self.get_ranged_damage() - params[0].damage_reduction)
        else:
            print(self.name + " missed!")
        self.frame_count = self.attack_speed
        return True
