from random import randint

from file_handler import get_yaml_data, get_yaml_list

class RosterLists:
    roster_dictionary = {}
    monster_dictionary = {}
    def build_roster_lists(self):
        #These two should be dynamically generated instead
        habitats = ['cave', 'dungeon', 'world']
        difficulty_levels = [1, 2]
        for h in habitats:
            for d in difficulty_levels:
                roster_loader = get_yaml_list(h, d, 'monsters')
                roster_name = h + str(d)
                self.roster_dictionary.update({roster_name:roster_loader})

    def build_monster_manual(self):
        self.monster_dictionary = get_yaml_data('name', 'none', 'monsters', 'full')

    def get_roster_lists(self):
        return self.roster_dictionary

    def get_monster_manual(self):
        return self.monster_dictionary

def gen_monster(monster_name, current_mm):
    for d in current_mm:
        if list(d)[0] == monster_name:
            return d.get(monster_name)

def roll_monster(habitat, current_roster):
    diff_roll = randint(1, 100)
    if diff_roll < 80:
        roster_name = habitat + str(1)
        roster_loader = current_roster.get(roster_name) 
        select_roll = randint(0, len(roster_loader)-1)
        monster_name = roster_loader[select_roll]
    else:
        roster_name = habitat + str(2)
        roster_loader = current_roster.get(roster_name)
        select_roll = randint(0, len(roster_loader)-1)
        monster_name = roster_loader[select_roll]
    return monster_name

#cr = RosterLists()
#cr.build_monster_manual()
#current_mm = cr.get_monster_manual()
#print(current_mm)
#m_loader = gen_monster('Troll', current_mm)
#print(m_loader['display_name'])
