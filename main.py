import random
from time import sleep


class Character:
    def __init__(self, name, health, shield, weapon = None):
        self.name = name
        self.health = health
        self.shield = shield
        self.weapon = weapon
        if weapon is None:
            self.weapon = Weapon("Brak broni", 0, 0)

    def character_stats(self):
        print("====================")
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Shield: {self.shield}")
        print(f"Weapon: {self.weapon.name}")
        print("====================")

    def is_alive(self):
        return self.health > 0

class Weapon:
    def __init__(self, name, attack_power, critical):
        self.name = name
        self.attack_power = attack_power
        self.critical = critical

    def weapon_stats(self):
        print("----------⚔️----------")
        print(f"Name: {self.name}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Critical: {self.critical}")
        print("----------⚔️----------")


class Item:
    def __init__(self, name, effect_type, value, quantity):
        self.name = name
        self.effect_type = effect_type
        self.value = value
        self.quantity = quantity

heal_potion = Item("Mikstura Lecznicza", "heal", 20, 1)
shield_potion = Item("Mikstura Tarczy", "shield", 20, 1)
damage_potion = Item("Mikstura Wściekłości", "damage", 15, 1)

items = [heal_potion, shield_potion, damage_potion]

class Player(Character):
    def heal(self):
        r_heal = random.randint(5, 20)
        self.health += r_heal
        return f"{self.name} wyleczył się o {r_heal} HP. Ma teraz {self.health} HP."

    def defence(self):
        r_shld = random.randint(5, 15)
        self.shield += r_shld
        return f"{self.name} wzmocnił tarczę o {r_shld}. Ma teraz {self.shield} punktów tarczy."

    def attack(self, enemy):
        # szanse na krytyka
        critical = random.random() < self.weapon.critical
        damage = self.weapon.attack_power * (2 if critical else 1)

        if critical:
            enemy.shield = 0
            enemy.health -= damage
            if enemy.health < 0:
                enemy.health = 0
            return f"💥 {self.name} zadał obrażenia KRYTYCZNE! Zniszczył całą tarczę i zadał {damage} obrażeń. | HP wroga: {enemy.health}"

        # Normalny atak
        if enemy.shield > 0:
            if enemy.shield >= damage:
                enemy.shield -= damage
                return f"{self.name} uderzył w tarczę przeciwnika za {damage}. Tarcza przeciwnika: {enemy.shield}"
            else:
                # przebicie tarczy
                overflow = damage - enemy.shield
                enemy.shield = 0
                enemy.health -= overflow
                if enemy.health < 0:
                    enemy.health = 0
                return f"{self.name} przebił tarczę i zadał {overflow} obrażeń w HP! | HP wroga: {enemy.health}"
        else:
            enemy.health -= damage
            if enemy.health < 0:
                enemy.health = 0
            return f"{self.name} zadał {damage} obrażeń. | HP wroga: {enemy.health}"

    def check_stats(self):
        self.character_stats()

    def check_enemy(self, enemy):
        enemy.character_stats()
    
    def check_items(self):
        choose_item = None
        while choose_item == None:
            try:
                for idx, item in enumerate(items):
                    print(f"{idx + 1}. {item.name} - {item.quantity}")
                print("0. Powrót")
                choose_item = int(input("Wybierz przedmiot: "))
                if choose_item not in range(0, len(items) + 1):
                    print("\033[91mNieprawidłowy wybór.\033[0m")
                    choose_item = None
                    continue
                if choose_item == 0:
                    break
                if items[choose_item - 1].quantity == 0:
                    print("\033[91mNie ma więcej tego przedmiotu.\033[0m")
                    choose_item = None
                else:
                    if items[choose_item - 1].effect_type == "heal":
                        self.health += items[choose_item - 1].value
                        items[choose_item - 1].quantity -= 1
                        print(f"\033[92m{self.name} wyleczył się o {items[choose_item - 1].value} HP. Ma teraz {self.health} HP.\033[0m")
                    elif items[choose_item - 1].effect_type == "shield":
                        self.shield += items[choose_item - 1].value
                        items[choose_item - 1].quantity -= 1
                        print(f"\033[94m{self.name} wzmocnił tarczę o {items[choose_item - 1].value}. Ma teraz {self.shield} punktów tarczy.\033[0m")
                    elif items[choose_item - 1].effect_type == "damage":
                        self.weapon.attack_power += items[choose_item - 1].value
                        items[choose_item - 1].quantity -= 1
                        print(f"\033[91m{self.name} zwiększył atak o {items[choose_item - 1].value}. Ma teraz {self.weapon.attack_power} obrażeń.\033[0m")
            except ValueError:
                print("\033[91mNieprawidłowy wybór.\033[0m")

        


class Enemy(Character):
    def attack(self, player):
        # szanse na unik gracza
        dodge = random.random() < self.weapon.critical
        if dodge:
            return f"{player.name} uniknął ataku {self.name}!"

        damage = self.weapon.attack_power
        if player.shield > 0:
            if player.shield >= damage:
                player.shield -= damage
                return f"{self.name} uderzył w tarczę {player.name} za {damage}. Tarcza gracza: {player.shield}"
            else:
                overflow = damage - player.shield
                player.shield = 0
                player.health -= overflow
                if player.health < 0:
                    player.health = 0
                return f"{self.name} przebił tarczę i zadał {overflow} obrażeń! | HP gracza: {player.health}"
        else:
            player.health -= damage
            if player.health < 0:
                player.health = 0
            return f"{self.name} zadał {damage} obrażeń {player.name}. | HP gracza: {player.health}"

    def defence(self):
        r_shld = random.randint(5, 15)
        self.shield += r_shld
        return f"{self.name} wzmocnił tarczę o {r_shld}. Ma teraz {self.shield} punktów tarczy."


# =========================
#     LOGIKA GRY
# =========================

weapons = [
    Weapon("Topór", 25, 0.2),
    Weapon("Miecz", 20, 0.35),
    Weapon("Sztylet", 15, 0.5),
    Weapon("Kieł", 12, 0.6),
]

enemies = [
    Enemy("Goblin", 70, 30, weapons[0]),
    Enemy("Ork", 120, 50, weapons[1]),
    Enemy("Rabuś", 30, 10, weapons[2]),
    Enemy("Wilk", 100, 0, weapons[3]),
]

bosses = [
    Enemy("Smok", 400, 50, Weapon("Ogień", 30, 0.2)),
    Enemy("Bazyliszek", 100, 600, Weapon("Ogon", 20, 0.8)),
]

if __name__ == "__main__":
    enemy = random.choice(enemies)
    tury = 0
    player = Player("Gracz", 100, 15)
    player.character_stats()
    enemy.character_stats()

    weapon_choice = None
    while weapon_choice == None:
        print("---- Wybór broni ----")
        for idx, weapon in enumerate(weapons):
            print(f"{idx + 1}. {weapon.name}")
        weapon_choose = int(input("Wybierz broń: "))
        try:
            weapon_choice = weapons[weapon_choose - 1]
            player.weapon = weapon_choice
            print("---------------------")
            print(f"\033[92mWybrano broń: {player.weapon.name}\033[0m")
            print("---------------------")
            
        except IndexError:
            print("\033[93m Nieprawidłowy wybór!\033[0m")


    print("---- POJEDYNEK ---")


    
    while player.is_alive() and enemy.is_alive():
        print(f"\n--- TURA {tury} ---")
        print("1. Atakuj\n2. Leczenie\n3. Obrona\n4. Ekwipunek\n5. Sprawdź statystyki")
        choice = input("Wybór: ")

        print("\nTrwa ruch...")
        sleep(1.2)

        if choice == "1":
            print("-----------------")
            print(player.attack(enemy))
            print("-----------------")
        elif choice == "2":
            print("-----------------")
            print(player.heal())
            print("-----------------")
        elif choice == "3":
            print("-----------------")
            print(player.defence())
            print("-----------------")
        elif choice == "4":
            print("-----------------")
            player.check_items()
            print("-----------------")
            continue
        elif choice == "5":
            print("-----------------")
            player.check_stats()
            player.check_enemy(enemy)
            print("-----------------")
            continue
        else:
            print("\nNieprawidłowy wybór!")
            continue

        if not enemy.is_alive() or not player.is_alive():
            break

        # Ruch przeciwnika
        print("\nRuch przeciwnika...")
        sleep(1.2)
        print('------------------------------')
        move = random.choice(["attack", "attack", "defence"])  # 2/3 szans na atak
        if move == "attack":
            print(f"{enemy.name} atakuje!")
            print(enemy.attack(player))
        elif move == "defence":
            print(f"{enemy.name} się broni!")
            print(enemy.defence())
        print('------------------------------')

        tury += 1

    # Wynik końcowy
    print("\n==============================")
    if not player.is_alive():
        print("❌ Gracz przegrał!")
    else:

        print("✅ Wygrałeś walkę!")
        boss_fight = False
        while boss_fight == False:
            choose = input("\nCzy chcesz zagrać w walkę z bossem? (t/n): ")
            if choose == "t":
                boss_fight = True
                enemy = random.choice(bosses)
                tury = 0
                player.character_stats()
                enemy.character_stats()
            elif choose == "n":
                print("Uciekanie do lasu...")
                sleep(3)
                print("\nDziękuję za grę!")
                break
    print("==============================")
