import random

class Enemy:
    def __init__(self, name, hp, attack, defense, level, exp_reward, gold_reward):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward


def get_random_enemy(player_level):
    tier_enemies = {
        (1, 10): [("Ironhide Boar", 60, 15, 5, 15, 10), ("Thorn Stalker", 50, 18, 4, 12, 8), ("Crystal Brute", 40, 10, 2, 10, 5),
                  ("Royal Executioner", 80, 12, 8, 20, 15), ("Iron Fortress Guard", 70, 16, 6, 18, 12)],
        (11, 20): [("Imperial Sentinel", 150, 35, 15, 45, 30), ("Magma Crawler", 130, 30, 12, 40, 35), ("Alpine Raptor", 200, 40, 20, 60, 50),
                   ("Stone Crusher", 120, 45, 10, 50, 40), ("Cave Berserker", 140, 38, 14, 55, 45)]
    }

    pool = []
    for (low, high), enemies in tier_enemies.items():
        if low <= player_level <= high:
            pool = enemies
            break
    if not pool:
        pool = [("Regional Monster", player_level * 25, player_level * 8, player_level * 4, player_level * 15,
                 player_level * 10)]

    data = random.choice(pool)
    scale = 1 + (player_level * 0.05)
    return Enemy(data[0], int(data[1] * scale), int(data[2] * scale), int(data[3] * scale), player_level,
                 int(data[4] * scale), int(data[5] * scale))


BOSSES = {
    10: {"name": "Goblin King", "hp": 350, "attack": 45, "defense": 15, "exp": 200, "gold": 150},
    20: {"name": "Forest Guardian", "hp": 700, "attack": 80, "defense": 30, "exp": 450, "gold": 350},
    30: {"name": "Ancient Golem", "hp": 1200, "attack": 120, "defense": 50, "exp": 800, "gold": 600},
    40: {"name": "Vampire Lord", "hp": 1800, "attack": 170, "defense": 70, "exp": 1200, "gold": 1000},
    50: {"name": "Dragon Rider", "hp": 2500, "attack": 220, "defense": 90, "exp": 2000, "gold": 1500},
    60: {"name": "Demon General", "hp": 3400, "attack": 280, "defense": 120, "exp": 3000, "gold": 2200},
    70: {"name": "Ice Titan", "hp": 4500, "attack": 350, "defense": 150, "exp": 4500, "gold": 3000},
    80: {"name": "Shadow Emperor", "hp": 6000, "attack": 420, "defense": 180, "exp": 6000, "gold": 4500},
    90: {"name": "Celestial Dragon", "hp": 8000, "attack": 500, "defense": 220, "exp": 8500, "gold": 6000},
    100: {"name": "Ancient Demon King", "hp": 12000, "attack": 650, "defense": 300, "exp": 20000, "gold": 15000}
}