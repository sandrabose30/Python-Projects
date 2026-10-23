class Item:
    def __init__(self, name, rarity, price, req_level):
        self.name = name
        self.rarity = rarity
        self.price = price
        self.req_level = req_level

    def to_dict(self):
        return self.__dict__

class Weapon(Item):
    def __init__(self, name, rarity, damage, crit_bonus, price, req_level):
        super().__init__(name, rarity, price, req_level)
        self.damage = damage
        self.crit_bonus = crit_bonus

class Armor(Item):
    def __init__(self, name, rarity, defense, hp_bonus, mana_bonus, crit_res, price, req_level):
        super().__init__(name, rarity, price, req_level)
        self.defense = defense
        self.hp_bonus = hp_bonus
        self.mana_bonus = mana_bonus
        self.crit_res = crit_res

class Potion(Item):
    def __init__(self, name, category, effect_value, price):
        super().__init__(name, "Common", price, 1)
        self.category = category  # 'health', 'mana', 'mixed', 'buff'
        self.effect_value = effect_value

WEAPON_POOL = [
    Weapon("Wooden Sword", "Common", 10, 0, 50, 1),
    Weapon("Rusty Axe", "Common", 12, 0, 60, 1),
    Weapon("Training Bow", "Common", 9, 2, 55, 1),
    Weapon("Iron Sword", "Rare", 25, 5, 200, 5),
    Weapon("Steel Axe", "Rare", 28, 5, 220, 5),
    Weapon("Long Bow", "Rare", 22, 8, 210, 5),
    Weapon("Crystal Blade", "Super Rare", 45, 8, 500, 10),
    Weapon("Shadow Dagger", "Super Rare", 42, 12, 480, 10),
    Weapon("Lightning Bow", "Super Rare", 40, 10, 490, 10),
    Weapon("Flame Sword", "Epic", 70, 12, 1200, 20),
    Weapon("Ice Spear", "Epic", 68, 10, 1150, 20),
    Weapon("Thunder Hammer", "Epic", 75, 15, 1300, 20),
    Weapon("Phoenix Blade", "Mythical", 110, 18, 3000, 35),
    Weapon("Demon Slayer", "Mythical", 115, 20, 3200, 35),
    Weapon("Celestial Staff", "Mythical", 105, 22, 3100, 35),
    Weapon("Dragon King's Sword", "Legendary", 160, 25, 7500, 50),
    Weapon("Blade of Eternity", "Legendary", 165, 25, 7800, 50),
    Weapon("Bow of the Gods", "Legendary", 155, 30, 7200, 50),
    Weapon("Void Reaper", "Legendary", 180, 35, 9000, 70),
    Weapon("Excalibur", "Legendary", 200, 40, 12000, 90)
]

ARMOR_POOL = [
    Armor("Cloth Tunic", "Common", 5, 20, 10, 0, 40, 1),
    Armor("Leather Armor", "Uncommon", 12, 40, 20, 2, 100, 5),
    Armor("Chainmail", "Rare", 25, 80, 40, 4, 250, 10),
    Armor("Iron Cuirass", "Rare", 35, 100, 50, 5, 350, 15),
    Armor("Steel Plate", "Super Rare", 55, 150, 70, 8, 700, 25),
    Armor("Shadow Cloak", "Super Rare", 50, 120, 100, 12, 750, 25),
    Armor("Dragon Scale Armor", "Epic", 80, 250, 120, 15, 1500, 40),
    Armor("Mage Robes of Archon", "Epic", 70, 200, 250, 10, 1600, 40),
    Armor("Mythril Armor", "Mythical", 120, 400, 200, 20, 3500, 60),
    Armor("Celestial Armor", "Mythical", 130, 450, 250, 22, 4000, 70),
    Armor("Demon Armor", "Legendary", 180, 700, 350, 30, 8000, 85),
    Armor("Godly Divine Plate", "Legendary", 220, 1000, 500, 40, 12000, 95)
]

POTION_POOL = [
    Potion("Small HP Potion", "health", 50, 20),
    Potion("Medium HP Potion", "health", 100, 50),
    Potion("Large HP Potion", "health", 250, 120),
    Potion("Giant HP Potion", "health", 500, 250),
    Potion("Ultimate HP Potion", "health", 9999, 500),
    Potion("Small Mana Potion", "mana", 30, 20),
    Potion("Medium Mana Potion", "mana", 75, 45),
    Potion("Large Mana Potion", "mana", 150, 100),
    Potion("Giant Mana Potion", "mana", 300, 200),
    Potion("Ultimate Mana Potion", "mana", 9999, 450),
    Potion("Mixed Elixir", "mixed", 200, 150),
    Potion("Greater Mixed Elixir", "mixed", 500, 350),
    Potion("Attack Buff Potion", "buff", 15, 100),
    Potion("Defense Buff Potion", "buff", 15, 100),
    Potion("Critical Buff Potion", "buff", 10, 120)
]