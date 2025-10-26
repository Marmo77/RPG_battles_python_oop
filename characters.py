# characters.py
import random
from typing import List
from weapons import Weapon
from items import Item


class Character:
    def __init__(self, name: str, health: int, shield: int, weapon: Weapon = None):
        self.name = name
        self.health = health
        self.shield = shield
        self.weapon = weapon if weapon is not None else Weapon("Brak broni", 0, 0.0)
        self.effects = []  # lista efektów statusowych: dicty {type, turns, value}

    def character_stats(self):
        print("====================")
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Shield: {self.shield}")
        print(f"Weapon: {self.weapon.name} (ATK: {self.weapon.attack_power})")
        if self.effects:
            print("Effects:", self.effects)
        print("====================")

    def is_alive(self) -> bool:
        return self.health > 0

    def apply_effects(self):
        """Zastosuj efekty (np. poison) i zmniejsz liczbę tur."""
        new_effects = []
        for e in self.effects:
            if e["type"] == "poison":
                self.health -= e["value"]
                print(f"\033[91m{self.name} traci {e['value']} HP od zatrucia ({e['turns']} tury pozostało).\033[0m")
            # więcej typów można dopisać tutaj
            e["turns"] -= 1
            if e["turns"] > 0:
                new_effects.append(e)
        self.effects = new_effects
        if self.health < 0:
            self.health = 0


class Player(Character):
    def __init__(self, name: str, health: int, shield: int, weapon: Weapon = None, inventory: List[Item] = None):
        super().__init__(name, health, shield, weapon)
        self.inventory = inventory if inventory is not None else []
        self.level = 1
        self.exp = 0
        self.gold = 0

    def heal(self):
        r_heal = random.randint(5, 20)
        self.health += r_heal
        return f"{self.name} wyleczył się o {r_heal} HP. Ma teraz {self.health} HP."

    def defence(self):
        r_shld = random.randint(5, 15)
        self.shield += r_shld
        return f"{self.name} wzmocnił tarczę o {r_shld}. Ma teraz {self.shield} punktów tarczy."

    def attack(self, enemy: Character):
        critical = random.random() < self.weapon.critical
        damage = self.weapon.attack_power * (2 if critical else 1)

        if critical:
            enemy.shield = 0
            enemy.health -= damage
            enemy.health = max(0, enemy.health)
            return f"💥 {self.name} zadał obrażenia KRYTYCZNE! Zniszczył tarczę i zadał {damage} obrażeń. | HP wroga: {enemy.health}"

        # normalny atak (obsługa tarczy -> overflow do HP)
        if enemy.shield > 0:
            if enemy.shield >= damage:
                enemy.shield -= damage
                return f"{self.name} uderzył w tarczę przeciwnika za {damage}. Tarcza przeciwnika: {enemy.shield}"
            else:
                overflow = damage - enemy.shield
                enemy.shield = 0
                enemy.health -= overflow
                enemy.health = max(0, enemy.health)
                return f"{self.name} przebił tarczę i zadał {overflow} obrażeń w HP! | HP wroga: {enemy.health}"
        else:
            enemy.health -= damage
            enemy.health = max(0, enemy.health)
            return f"{self.name} zadał {damage} obrażeń. | HP wroga: {enemy.health}"

    def check_stats(self):
        self.character_stats()

    def check_enemy(self, enemy: Character):
        enemy.character_stats()

    def check_items(self):
        """Interaktywny wybór przedmiotu z inventory (użycie)."""
        if not self.inventory:
            print("\033[93mEkwipunek pusty.\033[0m")
            return
        while True:
            try:
                print("---- EKWIPUNEK ----")
                for idx, item in enumerate(self.inventory):
                    print(f"{idx + 1}. {item.name} ({item.effect_type} {item.value}) x{item.quantity}")
                print("0. Powrót")
                choice = int(input("Wybierz przedmiot: "))
                if choice == 0:
                    return
                if not (1 <= choice <= len(self.inventory)):
                    print("\033[91mNieprawidłowy wybór.\033[0m")
                    continue
                it = self.inventory[choice - 1]
                if it.quantity <= 0:
                    print("\033[91mNie ma tego przedmiotu.\033[0m")
                    continue
                # zastosuj efekt
                if it.effect_type == "heal":
                    self.health += it.value
                    print(f"\033[92m{self.name} wyleczył się o {it.value} HP. Ma teraz {self.health} HP.\033[0m")
                elif it.effect_type == "shield":
                    self.shield += it.value
                    print(f"\033[94m{self.name} wzmocnił tarczę o {it.value}. Ma teraz {self.shield} punktów tarczy.\033[0m")
                elif it.effect_type == "damage":
                    self.weapon.attack_power += it.value
                    print(f"\033[91m{self.name} zwiększył atak o {it.value}. Ma teraz {self.weapon.attack_power} obrażeń.\033[0m")
                elif it.effect_type == "poison":
                    # użycie przedmiotu dodaje efekt na wroga: tu placeholder, lepiej wywołać z battle
                    pass
                it.quantity -= 1
                return
            except ValueError:
                print("\033[91mNieprawidłowy wybór.\033[0m")


class Enemy(Character):
    def __init__(self, name: str, health: int, shield: int, weapon: Weapon = None):
        super().__init__(name, health, shield, weapon)
        self.enraged = False  # przydatne dla bossów

    def attack(self, player: Player):
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
                player.health = max(0, player.health)
                return f"{self.name} przebił tarczę i zadał {overflow} obrażeń! | HP gracza: {player.health}"
        else:
            player.health -= damage
            player.health = max(0, player.health)
            return f"{self.name} zadał {damage} obrażeń {player.name}. | HP gracza: {player.health}"

    def defence(self):
        r_shld = random.randint(5, 15)
        self.shield += r_shld
        return f"{self.name} wzmocnił tarczę o {r_shld}. Ma teraz {self.shield} punktów tarczy."
