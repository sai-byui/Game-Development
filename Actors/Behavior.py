class Behavior:
    def __init__(self, name, callback=None, callback_parameters=[]):
        self.name = name
        self.is_bottom_level = True  # False if sub_behaviors is populated, true if callback != None
        self.sub_behaviors = []  # List of actions to be taken as part of this action
        self.callback = callback  # Function to call if bottom level
        self.callback_parameters = callback_parameters

    def perform_action(self, actor):
        if self.is_bottom_level:
            if self.callback(self.callback_parameters):
                return True
            return False
        else:
            if not self.sub_behaviors:
                return True
            else:
                if self.sub_behaviors[0].perform_action(actor):
                    self.sub_behaviors.remove(self.sub_behaviors[0])
                return False

