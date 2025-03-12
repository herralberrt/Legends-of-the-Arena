# Legends of the Arena -> Powered by Romaniuc Albert-Iulian

"""
Battle Quest: The Arena - Game Description 

Welcome to Battle Quest: The Arena, a turn-based RPG where you fight against powerful enemies, upgrade your character, and survive as long as possible!

How to Play:
1. Choose Your Character - Pick from a variety of heroes, each with unique stats and special abilities.
2. Fight in the Arena - Face random enemies in intense battles. You can:
   - Attack to deal damage.
   - Drink a potion to restore health.
   - Defend to reduce damage from the next enemy attack.
   - Use your special ability for a powerful move!
3. Survive & Earn Points - Winning battles gives you score points based on your health and progress.
4. Visit the Shop - After each battle, you can buy weapons, armor, and potions using your earned points.
5. Continue Fighting - The game keeps going until you lose all your health.

Goal:
Defeat as many enemies as possible, upgrade your gear, and see how long you can survive in the arena!

Do you have what it takes to become the ultimate champion? 
"""

import random
import time

# ============================
#        Player Class
# ============================
class Player:
    def __init__(self, name, health, attack, potions, special_ability):
        """Initialize a player with stats and abilities."""
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.potions = potions
        self.weapon = None  # Default: No weapon equipped
        self.armor = None   # Default: No armor equipped
        self.armor_defense = 0  # Armor reduces damage taken
        self.defense = False
        self.special_ability = special_ability
        self.special_used = False
        self.score = 0  # Score = in-game currency

    def equip_weapon(self, weapon_name, attack_boost, cost):
        """Equip a weapon to increase attack power."""
        if self.score >= cost:
            if self.weapon:
                print(f"You replaced {self.weapon} with {weapon_name}.")
            else:
                print(f"You equipped {weapon_name}!")
            self.weapon = weapon_name
            self.attack += attack_boost
            self.score -= cost
            print(f"Attack increased by {attack_boost}. Remaining points: {self.score}")
        else:
            print("Not enough points to buy this weapon.")

    def equip_armor(self, armor_name, defense_boost, cost):
        """Equip armor to reduce damage taken."""
        if self.score >= cost:
            if self.armor:
                print(f"You replaced {self.armor} with {armor_name}.")
            else:
                print(f"You equipped {armor_name}!")
            self.armor = armor_name
            self.armor_defense = defense_boost
            self.score -= cost
            print(f"Armor reduces damage by {defense_boost}. Remaining points: {self.score}")
        else:
            print("Not enough points to buy this armor.")

    def attack_enemy(self, enemy):
        """Perform an attack with damage calculation, considering armor and defense."""
        if self.health <= 0 or enemy.health <= 0:
            return  # Dead players or enemies cannot attack

        base_damage = random.randint(1, self.attack)

        if enemy.defense:
            base_damage //= 2  # Reduce damage if the enemy is defending
            enemy.defense = False
            print(f"{enemy.name} blocked the attack! Damage reduced to {base_damage}.")

        if enemy.armor_defense > 0:
            base_damage = max(base_damage - enemy.armor_defense, 0)
            print(f"{enemy.name}'s armor absorbs {enemy.armor_defense} damage!")

        enemy.health -= base_damage
        print(f"{self.name} attacks {enemy.name} for {base_damage} damage!")

        if enemy.health <= 0:
            print(f"{enemy.name} has been defeated!")

    def drink_potion(self):
        """Heal using a potion if available and needed."""
        if self.potions > 0:
            if self.health == self.max_health:
                print(f"{self.name} is already at full health and wasted a potion!")
                return
            healing = random.randint(10, 30)
            self.health = min(self.health + healing, self.max_health)
            self.potions -= 1
            print(f"{self.name} drinks a potion and heals {healing} HP! ({self.potions} left)")
        else:
            print(f"{self.name} has no potions left!")

    def activate_defense(self):
        """Defend to reduce damage next turn."""
        self.defense = True
        print(f"{self.name} is preparing to block the next attack!")

    def use_special(self, enemy):
        """Use the character's special ability."""
        if self.special_used:
            print("Special ability already used!")
            return

        self.special_used = True

        if self.special_ability == "Power Strike":
            damage = self.attack * 2
        elif self.special_ability == "Fireball":
            damage = random.randint(self.attack + 5, self.attack + 15)
        elif self.special_ability == "Holy Light":
            healing = random.randint(20, 40)
            self.health = min(self.health + healing, self.max_health)
            print(f"{self.name} uses Holy Light! Heals {healing} HP!")
            return
        elif self.special_ability == "Shadow Strike":
            damage = random.randint(self.attack + 10, self.attack + 20)
        elif self.special_ability == "Rage Mode":
            self.attack += 5
            print(f"{self.name} enters Rage Mode! Attack increased permanently!")
            return
        else:
            print("No special ability available!")
            return

        enemy.health -= damage
        print(f"{self.name} uses {self.special_ability} and deals {damage} damage!")

    def is_alive(self):
        """Check if the player is still alive."""
        return self.health > 0


# ============================
#         Shop System
# ============================
def shop(player):
    """Allow the player to buy items using their score."""
    print("\n--- Welcome to the Shop! ---")
    print(f"Your current score: {player.score} points")
    print("1 - Buy a Potion (50 points)")
    print("2 - Buy a Sword (+5 Attack) (100 points)")
    print("3 - Buy a Shield (-5 Damage Taken) (100 points)")
    print("4 - Buy a Greatsword (+10 Attack) (200 points)")
    print("5 - Buy Heavy Armor (-10 Damage Taken) (200 points)")
    print("6 - Exit Shop")

    while True:
        choice = input("Choose an option: ")
        if choice == "6":
            break
        elif choice == "1" and player.score >= 50:
            player.potions += 1
            player.score -= 50
            print("You bought a potion!")
        elif choice == "2" and player.score >= 100:
            player.equip_weapon("Sword", 5, 100)
        elif choice == "3" and player.score >= 100:
            player.equip_armor("Shield", 5, 100)
        elif choice == "4" and player.score >= 200:
            player.equip_weapon("Greatsword", 10, 200)
        elif choice == "5" and player.score >= 200:
            player.equip_armor("Heavy Armor", 10, 200)
        else:
            print("Invalid choice or not enough points!")


# ============================
#        Main Game Loop
# ============================
def game():
    """Main game function where the player fights enemies and progresses."""
    start_time = time.time()

    characters = {
        "1": Player("Warrior", 100, 20, 3, "Power Strike"),
        "2": Player("Mage", 80, 25, 5, "Fireball"),
        "3": Player("Orc", 120, 15, 2, "Rage Mode"),
        "4": Player("Paladin", 110, 18, 4, "Holy Light"),
        "5": Player("Assassin", 90, 22, 3, "Shadow Strike")
    }

    enemies = [
        Player("Goblin", 90, 14, 2, "Poison Strike"),
        Player("Vampire", 120, 22, 4, "Life Drain"),
        Player("Dragon", 150, 18, 3, "Flame Breath"),
        Player("Golem", 180, 12, 3, "Stone Shield")
    ]

    print("\nAvailable Characters:")
    for key, char in characters.items():
        print(f"{key} - {char.name} (HP: {char.health}, Attack: {char.attack}, Potions: {char.potions}) - Special: {char.special_ability}")

    print("\nAvailable Enemies:")
    for i, enemy in enumerate(enemies, start=1):
        print(f"{i} - {enemy.name} (HP: {enemy.health}, Attack: {enemy.attack}, Potions: {enemy.potions}) - Special: {enemy.special_ability}")

    choice = input("\nChoose your character: ")
    player = characters.get(choice, characters["1"])

    print(f"\nYou have chosen {player.name}!\n")

    round_number = 1
    while player.is_alive():
        enemy = random.choice(enemies)
        print(f"\n--- Round {round_number}: You will fight {enemy.name}! ---\n")

        while player.is_alive() and enemy.is_alive():
            print("\n1 - Attack\n2 - Drink a potion\n3 - Defend\n4 - Use Special Ability")
            choice = input("Choose an action: ")
            if choice == "1":
                player.attack_enemy(enemy)
            elif choice == "2":
                player.drink_potion()
            elif choice == "3":
                player.activate_defense()
            elif choice == "4":
                player.use_special(enemy)

        if player.is_alive():
            player.score += 100 + player.health
            shop(player)
            round_number += 1

    print(f"\nGame Over! You played for {round(time.time() - start_time, 2)} seconds. Thanks for playing!")
    
if __name__ == "__main__":
    game()
