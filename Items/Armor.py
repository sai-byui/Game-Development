from Items.Equipment import Equipment, Slots

class Armor(Equipment):
    def __init__(self):
        super(Armor, self).__init__()
        self.armor_class_bonus = 0.05
        self.speed_multiplier = 1.0