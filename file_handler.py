import sys
from ruamel.yaml import YAML

#Getting the d for a single element from the list
def get_yaml_data(key, value, list_name):
    if list_name == 'monster':
        #Open a file stream
        input_file = open("data_files/monsters.yaml").read()
        #Create the yaml object
        yaml=YAML(typ="safe", pure=True)
        #Load our input stream
        monster_list=yaml.load(input_file)
        
        for d in monster_list:
            if key in d and d.get(key) == value:
                return d

#OTHER EXAMPLES
#Iterate through the whole list and print each of the key / value pairs
#for listing in monster:
#    for key, value in listing.items():
#        print(key, ":", value)

#print(get_yaml_data('name', 'troll', monster))
#monster_loader = get_yaml_data('name', 'troll', monster)
#print(monster_loader['name'])
