from Items.Armor import Armor
import random

class Shield(Armor):
    def __init__(self):
        super(Shield, self).__init__()
        self.inventory_space = 6
        self.name = "Shield"  #Generate random mods later
        self.armor_class_bonus = random.uniform(0.05, 0.25)
        self.speed_multiplier = 0.9
        self.slot = self.Slots.Offhand_slot