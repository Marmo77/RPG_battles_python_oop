# battles.py
import random
from time import sleep
from characters import Player, Enemy
from items import Item

def battle(player: Player, enemy: Enemy, allow_items_in_battle: bool = True) -> bool:
    """
    Prowadzi pojedynek między player a enemy.
    Zwraca True jeżeli gracz wygrał, False jeżeli przegrał.
    """
    tury = 1
    print("---- POJEDYNEK ---")
    player.character_stats()
    enemy.character_stats()

    while player.is_alive() and enemy.is_alive():
        print(f"\n--- TURA {tury} ---")
        # apply status effects at start of turn
        player.apply_effects()
        enemy.apply_effects()

        print("1. Atakuj\n2. Leczenie\n3. Obrona")
        if allow_items_in_battle:
            print("4. Ekwipunek")
            print("5. Sprawdź statystyki")
            print("6. Zapisz stan gry i wyjdź")
        else:
            print("4. Sprawdź statystyki")
        choice = input("Wybór: ")

        print("\nTrwa ruch...")
        sleep(0.8)

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
        elif allow_items_in_battle and choice == "4":
            print("-----------------")
            player.check_items()
            print("-----------------")
            # jeśli użył itemu to nie od razu kończ turę (opcjonalne)
        elif allow_items_in_battle and choice == "5":
            print("-----------------")
            player.check_stats()
            player.check_enemy(enemy)
            print("-----------------")
            # nie przechodzimy do tury przeciwnika, zostajemy w tej turze
            continue
        elif not allow_items_in_battle and choice == "4":
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

        # ruch przeciwnika
        print("\nRuch przeciwnika...")
        sleep(0.9)
        print('------------------------------')
        move = random.choice(["attack", "attack", "defence"])  # 2/3 atak
        if move == "attack":
            print(f"{enemy.name} atakuje!")
            print(enemy.attack(player))
        else:
            print(f"{enemy.name} się broni!")
            print(enemy.defence())
        print('------------------------------')

        tury += 1

    # wynik
    if player.is_alive():
        print("\n✅ Wygrałeś walkę!")
        return True
    else:
        print("\n❌ Przegrałeś walkę.")
        return False

def boss_battle(player: Player, boss: Enemy) -> bool:
    """
    Boss fight z prostą fazą: po osiągnięciu 50% HP boss enrages (zwiększa atak).
    """
    tury = 1
    print("---- WALKA Z BOSSEM ---")
    player.character_stats()
    boss.character_stats()

    while player.is_alive() and boss.is_alive():
        print(f"\n--- TURA {tury} ---")
        player.apply_effects()
        boss.apply_effects()

        # faza bossa
        if not boss.enraged and boss.health <= boss.health / 2:
            # Uwaga: powyższe porównanie nie zadziała jak tu napisane (wczytasz oryginalne HP)
            # Zamiast tego sprawdzamy procent z max (jeśli chcesz max_hp musisz dodać atrybut)
            pass

        # prosty input like in battle
        print("1. Atakuj\n2. Leczenie\n3. Obrona\n4. Ekwipunek\n5. Sprawdź statystyki")
        choice = input("Wybór: ")
        print("\nTrwa ruch...")
        sleep(0.8)

        if choice == "1":
            print(player.attack(boss))
        elif choice == "2":
            print(player.heal())
        elif choice == "3":
            print(player.defence())
        elif choice == "4":
            player.check_items()
        elif choice == "5":
            player.check_stats()
            boss.character_stats()
            continue
        else:
            print("Nieprawidłowy wybór.")
            continue

        # Boss specjalna faza: jeśli HP spadnie poniżej 50% jego początkowego (zaimplementujemy prostą metodę)
        # Aby to działało poprawnie, zaimplementujemy prostą "max_health" property w bossie w mainie przy tworzeniu
        if hasattr(boss, "max_health") and not boss.enraged:
            if boss.health <= boss.max_health * 0.5:
                boss.enraged = True
                boss.weapon.attack_power = int(boss.weapon.attack_power * 1.5)
                print("\033[91mBoss wpadł w szał! Jego atak wzrósł.\033[0m")

        # przeciwnik atakuje
        if boss.is_alive():
            print("\nRuch bossa...")
            sleep(0.9)
            move = random.choice(["attack", "attack", "defence"])
            if move == "attack":
                print(boss.attack(player))
            else:
                print(boss.defence())

        tury += 1

    if player.is_alive():
        print("\n✅ Pokonałeś bossa!")
        return True
    else:
        print("\n❌ Zostałeś pokonany przez bossa.")
        return False
