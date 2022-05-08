class Hero:
    xp_requirements = {5, 15, 25, 50, 75, 100, 125, 175, 225}

    def __init__(self, name, hero_class):
        self.name = name
        self.hero_class = hero_class
        self.hero_inventory = [None]
        self.gold = 50
        self.hero_level = 1
        self.hero_exp = 0
        self.hero_baseline_health = 10

    def set_hero_class(self, hero_class):
        self.hero_class = hero_class

    def set_hero_level(self, hero_level):
        self.hero_level = hero_level

    def set_hero_gold(self, amnt):
        self.gold = amnt  

    def get_hero_class(self):
        return self.hero_class

    def get_hero_level(self):
        return self.hero_level

    def get_hero_gold(self):
        return self.gold

    def level_up(self):
        pass

    def set_hero_exp(self, exp):
        self.hero_exp = exp
        self.level_up()

    def display_hero(self):
        print(f"Hero Name:{self.name}\tHero Class:{self.hero_class}\tHero Level (L:E):{self.hero_level}:{self.hero_exp}")    
