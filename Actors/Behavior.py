class Behavior:
    def __init__(self, name, callback=None, callback_parameters=None):
        self.name = name
        self.is_bottom_level = True  # False if sub_behaviors is populated, true if callback != None
        self.sub_behaviors = []  # List of actions to be taken as part of this action
        self.callback = callback  # Function to call if bottom level
        self.callback_parameters = callback_parameters

    def perform_action(self, actor):
        if self.is_bottom_level:
            command_string = "actor." + self.callback.__name__ + "("

        else:
            pass
