class Player:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.gold = 100

        # Set base stats based on chosen class[cite: 4]
        self._init_class_stats(class_type)

        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.bosses_defeated = []
        self.enemies_defeated = 0
        self.is_defending = False
        self.buff_turns = 0
        self.active_buff = None

    def _init_class_stats(self, c_type):
        if c_type == "Warrior":
            self.max_hp, self.hp = 150, 150
            self.max_mana, self.mana = 40, 40
            self.attack, self.defense, self.crit_chance = 25, 20, 5
        elif c_type == "Mage":
            self.max_hp, self.hp = 100, 100
            self.max_mana, self.mana = 120, 120
            self.attack, self.defense, self.crit_chance = 35, 8, 10
        elif c_type == "Archer":
            self.max_hp, self.hp = 120, 120
            self.max_mana, self.mana = 70, 70
            self.attack, self.defense, self.crit_chance = 30, 12, 20
        elif c_type == "Assassin":
            self.max_hp, self.hp = 90, 90
            self.max_mana, self.mana = 60, 60
            self.attack, self.defense, self.crit_chance = 40, 5, 35

    def get_skills(self):
        skills = {
            "Warrior": {"Slash": (10, 1.5), "Shield Bash": (15, 1.2), "Rage": (20, 2.0), "Earthquake": (35, 3.0)},
            "Mage": {"Fireball": (20, 1.6), "Ice Blast": (25, 1.8), "Thunder Strike": (35, 2.5), "Meteor": (50, 3.5)},
            "Archer": {"Multi Shot": (15, 1.4), "Poison Arrow": (20, 1.6), "Explosive Arrow": (30, 2.2),
                       "Sniper Shot": (40, 3.0)},
            "Assassin": {"Backstab": (15, 1.8), "Smoke Bomb": (20, 1.2), "Shadow Strike": (30, 2.5),
                         "Instant Kill": (50, 5.0)}
        }
        return skills.get(self.class_type, {})

    def gain_exp(self, amount):
        self.exp += amount
        print(f"Gained {amount} EXP.")
        while self.exp >= self.exp_to_level:
            self.exp -= self.exp_to_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp_to_level = int(self.exp_to_level * 1.3)
        self.max_hp += 25
        self.hp = self.max_hp
        self.max_mana += 15
        self.mana = self.max_mana
        self.attack += 5
        self.defense += 4
        print(f"\n🎉 LEVEL UP! You reached Level {self.level}!")