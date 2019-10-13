class Fighter:
    def __init__(self, hp, protection, power):
        self.max_hp = hp
        self.hp = hp #Initial HP
        self.protection = protection #Reduces incoming damage
        self.power = power #Potential damage

    def take_damage(self, amount):
        #List to store the results of damage
        results = []
        #Record any damage taken
        self.hp -= amount
        #If hp drops below zero mark the entity as dead
        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        #List to store the results of damage
        results = []
        #Calcluate damage taken
        damage = self.power - target.fighter.protection
        #Append the results depending on outcome
        if damage > 0:
            results.append({'message': '{0} attacks {1} for {2} hit points.'.format(self.owner.name.capitalize(), target.name, str(damage))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': '{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name)})

        return results
