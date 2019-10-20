import sys
from ruamel.yaml import YAML

#Getting the d for a single element from the list
def get_yaml_data(key, value, list_name, option):
    if list_name == 'monsters':
        input_file = open("data_files/monsters.yaml").read() #Open a file stream
        yaml=YAML(typ="safe", pure=True) #Create the yaml object
        monster_list=yaml.load(input_file) #Load our input stream

        if option == 'single':
            for d in monster_list: #Iterate through list of dictionaries
                if list(d)[0] == value: #Compare bare entry vs value
                    return d.get(value) #Return dictionary instead of key:value
        elif option == 'full':
            return monster_list 

def get_yaml_list(habitat, difficulty, list_name):
    if list_name == 'monsters':
        input_file = open("data_files/monsters.yaml").read() #Open a file stream
        yaml=YAML(typ="safe", pure=True) #Create the yaml object
        monster_list=yaml.load(input_file) #Load our input stream

        results_list = []
        for d in monster_list: #Iterate through list of dictionaries
            monster_entry = d.get(list(d)[0])
            entry_habitat = monster_entry.get('habitat')
            entry_difficulty = monster_entry.get('difficulty')
            for h in entry_habitat:
                if habitat == h and entry_difficulty == difficulty:
                    results_list.append(list(d)[0]) #Append bare value
        return results_list #Return habitat and diff filtered result list   

#OTHER EXAMPLES
#Iterate through the whole list and print each of the key / value pairs
#for listing in monster:
#    for key, value in listing.items():
#        print(key, ":", value)

#roster_loader = get_yaml_list('cave', 2, 'monsters')
#print(roster_loader)
#monster_loader = get_yaml_data('display_name', 'Troll', 'monsters')
#print(monster_loader)
