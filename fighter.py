class Fighter:
    def __init__(self, hp, protection, damage):
        self.max_hp = hp
        self.hp = hp #Initial HP
        self.protection = protection #Reduces incoming damage
        self.damage = damage
