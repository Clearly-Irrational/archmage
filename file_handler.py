import sys
from ruamel.yaml import YAML

#Getting the d for a single element from the list
def get_yaml_data(key, value, list_name):
    if list_name == 'monsters':
        input_file = open("data_files/monsters.yaml").read() #Open a file stream
        yaml=YAML(typ="safe", pure=True) #Create the yaml object
        monster_list=yaml.load(input_file) #Load our input stream

        for d in monster_list: #Iterate through list of dictionaries
            if list(d)[0] == value: #Compare bare entry vs value
                return d.get(value) #Return dictionary instead of key:value   

#OTHER EXAMPLES
#Iterate through the whole list and print each of the key / value pairs
#for listing in monster:
#    for key, value in listing.items():
#        print(key, ":", value)

#monster_loader = get_yaml_data('display_name', 'Troll', 'monster')
#print(monster_loader['hp'])
