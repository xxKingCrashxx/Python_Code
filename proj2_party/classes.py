class Class():
    def __init__(self):
        self.starting_gear = [None]
        self.class_health = 0
    pass

class Warrior(Class):
    def __init__(self):
        super().__init__()
        self.starting_gear = ["short sword", "chainmail", "buckler shield", "health potions", "rope", "rations"]
        self.class_health = 20
    


class Wizard(Class):
    def __init__(self):
        super().__init__()
        self.starting_gear = ["wooden staff", "robes", "spell book", "health potions", "rations", "spell materials"]
        self.class_health = 5

class Warlock(Class):
    def __init__(self):
        super().__init__()
        self.starting_gear = ["hatchet", "robes", "tomes", "health potions", "rations"]
        self.class_health = 10

class Rogue(Class):
    def __init__(self):
        super().__init__()
        self.starting_gear = ["duel daggers", "bow", "arrows", "smoke bombs", "health potions", "rations"]
        self.class_health = 10