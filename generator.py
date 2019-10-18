from random import randint

from file_handler import get_yaml_data, get_yaml_list

def gen_monster(monster_name):
    monster_info = get_yaml_data('name', monster_name, 'monsters')
    return monster_info

def roll_monster(habitat):
    #This method is not very efficient, I should generate each list once
    #on start then just import it here instead, works for now though
    diff_roll = randint(1, 100)
    if diff_roll < 80:
        roster_loader = get_yaml_list(habitat, 1, 'monsters')
        select_roll = randint(0, len(roster_loader)-1)
        monster_name = roster_loader[select_roll]
    else:
        roster_loader = get_yaml_list(habitat, 2, 'monsters')
        select_roll = randint(0, len(roster_loader)-1)
        monster_name = roster_loader[select_roll]
    return monster_name
