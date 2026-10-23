import json

def save_game(player, filename="savegame.json"):
    data = {
        "name": player.name,
        "class_type": player.class_type,
        "level": player.level,
        "exp": player.exp,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "mana": player.mana,
        "max_mana": player.max_mana,
        "gold": player.gold,
        "inventory": [i.to_dict() for i in player.inventory],
        "equipped_weapon": player.equipped_weapon.to_dict() if player.equipped_weapon else None,
        "equipped_armor": player.equipped_armor.to_dict() if player.equipped_armor else None,
        "bosses_defeated": player.bosses_defeated
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("💾 Game saved successfully!")

def load_game(filename="savegame.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Save file not found.")
        return None