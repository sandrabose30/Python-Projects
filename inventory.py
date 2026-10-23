from items import Weapon, Armor, Potion, WEAPON_POOL, ARMOR_POOL, POTION_POOL

def open_inventory(player):
    while True:
        print(f"\n--- INVENTORY & EQUIPMENT ---")
        print(f"Equipped Weapon: {player.equipped_weapon.name if player.equipped_weapon else 'None'}")
        print(f"Equipped Armor: {player.equipped_armor.name if player.equipped_armor else 'None'}")
        print(f"Gold: {player.gold} 🪙")
        print("1. View/Equip Items\n2. Back to Game")

        choice = input("Select choice: ").strip()
        if choice == '1':
            if not player.inventory:
                print("Your inventory is empty.")
                continue
            for idx, item in enumerate(player.inventory):
                print(f"{idx + 1}. {item.name} ({item.rarity})")
            eq_idx = int(input("Select item to equip/use (0 to cancel): ") or 0) - 1
            if 0 <= eq_idx < len(player.inventory):
                item = player.inventory[eq_idx]
                if isinstance(item, Weapon):
                    player.equipped_weapon = item
                    print(f"⚔️ Equipped {item.name}")
                elif isinstance(item, Armor):
                    player.equipped_armor = item
                    print(f"🛡️ Equipped {item.name}")
        else:
            break


def open_shop(player):
    while True:
        print(f"\n--- VILLAGE SHOP (Gold: {player.gold} 🪙) ---")
        print("1. Buy Weapons\n2. Buy Armor\n3. Buy Potions\n4. Exit Shop")
        choice = input("Select choice: ").strip()

        if choice == '1':
            for i, w in enumerate(WEAPON_POOL[:10]):
                print(f"{i + 1}. {w.name} [{w.rarity}] - {w.price} Gold")
            idx = int(input("Buy item number (0 to cancel): ") or 0) - 1
            if 0 <= idx < 10:
                item = WEAPON_POOL[idx]
                if player.gold >= item.price:
                    player.gold -= item.price
                    player.inventory.append(item)
                    print(f" Purchased {item.name}!")
                else:
                    print("❌ Not enough gold!")
        elif choice == '2':
            for i, a in enumerate(ARMOR_POOL[:6]):
                print(f"{i + 1}. {a.name} [{a.rarity}] - {a.price} Gold")
            idx = int(input("Buy item number (0 to cancel): ") or 0) - 1
            if 0 <= idx < 6:
                item = ARMOR_POOL[idx]
                if player.gold >= item.price:
                    player.gold -= item.price
                    player.inventory.append(item)
                    print(f" Purchased {item.name}!")
                else:
                    print("❌ Not enough gold!")
        elif choice == '3':
            for i, p in enumerate(POTION_POOL[:5]):
                print(f"{i + 1}. {p.name} - {p.price} Gold")
            idx = int(input("Buy item number (0 to cancel): ") or 0) - 1
            if 0 <= idx < 5:
                item = POTION_POOL[idx]
                if player.gold >= item.price:
                    player.gold -= item.price
                    player.inventory.append(item)
                    print(f" Purchased {item.name}!")
                else:
                    print("❌ Not enough gold!")
        else:
            break