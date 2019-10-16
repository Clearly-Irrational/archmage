from file_handler import get_yaml_data

def gen_monster(monster_name):
    monster_info = get_yaml_data('name', monster_name, 'monster')
    #print(monster_info)
    return monster_info

