from random import randint

from file_handler import get_yaml_data

def gen_monster(monster_name):
    monster_info = get_yaml_data('name', monster_name, 'monsters')
    #print(monster_info)
    return monster_info

def roll_monster():
    die_roll = randint(0, 100)
    if randint(0, 100) < 80:
        monster_name = 'Orc'
    else:
        monster_name = 'Troll'
    return monster_name
