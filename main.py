# main.py
import random
from time import sleep

from weapons import default_weapons
from items import default_items, Item
from characters import Player, Enemy
from battles import battle, boss_battle

# zdefiniuj listy przeciwników i bossów
weapons = default_weapons.copy()

enemies = [
    Enemy("Goblin", 70, 30, weapons[0]),
    Enemy("Ork", 120, 50, weapons[1]),
    Enemy("Rabuś", 30, 10, weapons[2]),
    Enemy("Wilk", 100, 0, weapons[3]),
]

bosses = [
    Enemy("Smok", 400, 50, weapons[0]),
    Enemy("Bazyliszek", 250, 60, weapons[1]),
]

# przypisz max_health dla bossów, potrzebne do faz
for b in bosses:
    b.max_health = b.health


def choose_weapon() -> object:
    choice = None
    while choice is None:
        print("---- Wybór broni ----")
        for idx, w in enumerate(weapons):
            print(f"{idx + 1}. {w.name} (ATK: {w.attack_power}, CRIT: {w.critical})")
        try:
            selected = int(input("Wybierz broń (liczba): "))
            if 1 <= selected <= len(weapons):
                return weapons[selected - 1]
            else:
                print("\033[93mNieprawidłowy wybór!\033[0m")
        except ValueError:
            print("\033[93mNieprawidłowy wybór!\033[0m")


def main():
    print("Witaj w konsolowej arenie!")
    sleep(0.8)

    # Stwórz gracza z domyślnym ekwipunkiem (kopiowanie, żeby avoid shared state)
    inv = [Item(it.name, it.effect_type, it.value, it.quantity) for it in default_items]
    player = Player("Gracz", 100, 15, inventory=inv)

    # wybór broni
    player.weapon = choose_weapon()
    print(f"\033[92mWybrano broń: {player.weapon.name}\033[0m")
    sleep(0.6)

    # losowy przeciwnik
    enemy = random.choice(enemies)

    # run battle
    won = battle(player, enemy, allow_items_in_battle=True)

    if not won:
        print("Koniec gry - spróbuj ponownie.")
        return

    # po zwycięstwie: nagroda (gold + drop)
    gained_gold = random.randint(10, 40)
    player.gold += gained_gold
    print(f"Zdobyłeś {gained_gold} złota! Masz teraz {player.gold} zł.")

    # losowy drop: mała szansa na nową broń
    if random.random() < 0.3:
        new_weapon = random.choice(weapons)
        print(f"\033[92mZnalazłeś broń: {new_weapon.name}! Chcesz ją wyposażyć? (t/n)\033[0m")
        ch = input().lower()
        if ch == "t":
            player.weapon = new_weapon
            print(f"Wyekwipowano: {player.weapon.name}")

    # zapytaj o walke z bossem
    while True:
        choose = input("\nCzy chcesz zagrać w walkę z bossem? (t/n): ").lower()
        if choose == "t":
            boss = random.choice(bosses)
            # przypisz max_health jeśli nie ma
            if not hasattr(boss, "max_health"):
                boss.max_health = boss.health
            boss_result = boss_battle(player, boss)
            if not boss_result:
                print("Zginąłeś w walce z bossem. Koniec gry.")
            else:
                print("Gratulacje! Otrzymujesz wyjątkową nagrodę.")
            break
        elif choose == "n":
            print("Uciekanie do lasu... (koniec gry)")
            sleep(1)
            break
        else:
            print("Wpisz 't' lub 'n'.")

    print("Dziękuję za grę!")


if __name__ == "__main__":
    main()
