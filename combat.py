import random
from items import Potion


def resolve_combat(player, enemy):
    print(f"\n⚔️ BATTLE START: {player.name} vs {enemy.name} (Level {enemy.level}) ⚔️")

    while player.hp > 0 and enemy.hp > 0:
        print(f"\n--- YOUR TURN ---")
        print(
            f"HP: {player.hp}/{player.max_hp} | Mana: {player.mana}/{player.max_mana} | Enemy HP: {enemy.hp}/{enemy.max_hp}")
        print("1. Attack\n2. Skills\n3. Use Potion\n4. Defend\n5. Run")

        choice = input("Choose action (1-5): ").strip()

        if choice == '1':
            dmg = max(1, (player.attack + (
                player.equipped_weapon.damage if player.equipped_weapon else 0)) - enemy.defense)
            crit = player.crit_chance + (player.equipped_weapon.crit_bonus if player.equipped_weapon else 0)
            if random.randint(1, 100) <= crit:
                dmg = int(dmg * 1.5)
                print("🔥 CRITICAL HIT! 🔥")
            enemy.hp -= dmg
            print(f"You dealt {dmg} damage to {enemy.name}.")

        elif choice == '2':
            skills = player.get_skills()
            print("Skills:", ", ".join([f"{k} (Mana: {v[0]})" for k, v in skills.items()]))
            s_choice = input("Enter skill name: ").strip()
            if s_choice in skills:
                cost, mult = skills[s_choice]
                if player.mana >= cost:
                    player.mana -= cost
                    dmg = max(5, int((player.attack * mult) - enemy.defense))
                    enemy.hp -= dmg
                    print(f"✨ Used {s_choice}! Dealt {dmg} damage.")
                else:
                    print("❌ Not enough mana!")
            else:
                print("❌ Invalid skill.")

        elif choice == '3':
            potions = [i for i in player.inventory if isinstance(i, Potion)]
            if not potions:
                print("❌ No potions in inventory!")
                continue
            for idx, p in enumerate(potions):
                print(f"{idx + 1}. {p.name} ({p.category})")
            p_idx = int(input("Select potion number: ") or 0) - 1
            if 0 <= p_idx < len(potions):
                pot = potions[p_idx]
                player.inventory.remove(pot)
                if pot.category == 'health':
                    player.hp = min(player.max_hp, player.hp + pot.effect_value)
                elif pot.category == 'mana':
                    player.mana = min(player.max_mana, player.mana + pot.effect_value)
                elif pot.category == 'mixed':
                    player.hp = min(player.max_hp, player.hp + pot.effect_value)
                    player.mana = min(player.max_mana, player.mana + pot.effect_value)
                print(f"🧪 Used {pot.name}!")

        elif choice == '4':
            player.is_defending = True
            print("🛡️ You take a defensive stance (50% damage reduction next turn).")

        elif choice == '5':
            if random.randint(1, 100) <= 50:
                print("🏃 Successfully ran away!")
                return "escaped"
            print("❌ Failed to escape!")

        if enemy.hp > 0:
            edmg = max(1,
                       enemy.attack - player.defense - (player.equipped_armor.defense if player.equipped_armor else 0))
            if player.is_defending:
                edmg = int(edmg * 0.5)
                player.is_defending = False
                print("🛡️ Defend mitigated incoming damage!")
            player.hp -= edmg
            print(f"{enemy.name} attacks you for {edmg} damage.")

    if player.hp <= 0:
        print("\n💀 You have been defeated...")
        return "defeat"
    else:
        print(f"\n🏆 Victory! You defeated {enemy.name}!")
        player.gain_exp(enemy.exp_reward)
        player.gold += enemy.gold_reward
        print(f"Collected {enemy.gold_reward} Gold!")
        return "victory"