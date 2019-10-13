import tcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        #List to store the results of damage
        results = []
        monster = self.owner
        #If the player can see the monster then the monster can see the player
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            #Move towards the player if not in melee range
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            #If in melee range then attack
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
