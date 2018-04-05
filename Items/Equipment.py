from Items.Item import Item

class Equipment(Item):
    def __init__(self):
        super(Equipment, self).__init__()
        self.slot = Slots.Main_Weapon
        self.durability = 100
        self.max_durability = 100


    class Slots:
        Head = 1
        Main_Weapon = 2
        Offhand_slot = 3
        Body_Armor = 4
        Legs = 5
        Feet = 6
        Ring1= 7
        Ring2 = 8
