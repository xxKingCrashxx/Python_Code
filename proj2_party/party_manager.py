from hero import Hero

class PartyManager():
    def __init__(self, *, party_name, size):
        """takes a party_name string and size integer to determine the maximum size a party can hold hero objects"""
        self.party_name = party_name
        self.party_members = [None] * size
    
    def add_hero(self, hero_object):
        """Method takes a hero object and adds it to the party"""

        self.party_members.append(hero_object)
        print('"{}" has been added to "{}"'.format(hero_object.name, self.party_name))

#testing functionality
hero1 = Hero("Gandalf", "wizard")
hero2 = Hero("Nitsua", "warlock")
hero3 = Hero("Eliff", "warrior")

party1 = PartyManager(party_name="band of the hawk", size=3)
party1.add_hero(hero1)
party1.add_hero(hero2)
party1.add_hero(hero3)

hero1.display_hero()
hero2.display_hero()
hero3.display_hero()