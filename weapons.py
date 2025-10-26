class Weapon:
    def __init__(self, name: str, attack_power: int, critical: float):
        self.name = name
        self.attack_power = attack_power
        self.critical = critical 

    def weapon_stats(self):
        print("----------⚔️----------")
        print(f"Name: {self.name}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Critical Chance: {self.critical * 100:.0f}%")
        print("----------⚔️----------")


default_weapons = [
    Weapon("Topór", 25, 0.2),
    Weapon("Miecz", 20, 0.35),
    Weapon("Sztylet", 15, 0.5),
    Weapon("Kieł", 12, 0.6),
]
