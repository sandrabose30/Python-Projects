from player import Player
from enemies import get_random_enemy, BOSSES, Enemy
from combat import resolve_combat
from inventory import open_inventory, open_shop
from world import get_current_region
from save_load import save_game, load_game


def main_menu():
    print("=" * 40)
    print("   LEGENDS OF THE FORGOTTEN REALM   ")
    print("=" * 40)
    print("1. New Game")
    print("2. Continue")
    print("3. Instructions")
    print("4. Exit")

    choice = input("Select option (1-4): ").strip()
    return choice


def run_game():
    player = None
    while True:
        choice = main_menu()
        if choice == '1':
            name = input("Enter Player Name: ").strip()
            print("Choose Your Class:\n1. Warrior\n2. Mage\n3. Archer\n4. Assassin")
            c_choice = input("Select class (1-4): ").strip()
            classes = {"1": "Warrior", "2": "Mage", "3": "Archer", "4": "Assassin"}
            player = Player(name, classes.get(c_choice, "Warrior"))
            break
        elif choice == '2':
            data = load_game()
            if data:
                player = Player(data["name"], data["class_type"])
                player.level = data["level"]
                player.exp = data["exp"]
                player.hp = data["hp"]
                player.max_hp = data["max_hp"]
                player.mana = data["mana"]
                player.max_mana = data["max_mana"]
                player.gold = data["gold"]
                break
        elif choice == '3':
            print(
                "\n[Instructions] Defeat monsters, level up every 10 levels to face regional bosses, and defeat the Ancient Demon King!")
        elif choice == '4':
            return

    # Game Loop
    while player and player.level <= 100:
        region = get_current_region(player.level)
        print(f"\n📍 Region: {region} | Level: {player.level} | Gold: {player.gold} 🪙")
        print("1. Explore & Fight Monster")
        print("2. Challenge Boss (Every 10 Levels)")
        print("3. Visit Shop")
        print("4. Inventory & Equipment")
        print("5. Save Game")
        print("6. Quit Game")

        act = input("Choose action (1-6): ").strip()

        if act == '1':
            enemy = get_random_enemy(player.level)
            result = resolve_combat(player, enemy)
            if result == "defeat":
                break
        elif act == '2':
            if player.level % 10 == 0 and player.level not in player.bosses_defeated:
                b_data = BOSSES[player.level]
                boss = Enemy(b_data["name"], b_data["hp"], b_data["attack"], b_data["defense"], player.level,
                             b_data["exp"], b_data["gold"])
                result = resolve_combat(player, boss)
                if result == "victory":
                    player.bosses_defeated.append(player.level)
            else:
                print("❌ No boss available at this level or already defeated!")
        elif act == '3':
            open_shop(player)
        elif act == '4':
            open_inventory(player)
        elif act == '5':
            save_game(player)
        elif act == '6':
            break

    if player and player.level >= 100 and 100 in player.bosses_defeated:
        print("\n🏆 CONGRATULATIONS! You defeated the Ancient Demon King and saved Eldoria!")


if __name__ == "__main__":
    run_game()