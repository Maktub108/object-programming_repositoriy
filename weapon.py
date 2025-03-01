from abc import ABC, abstractmethod
import random

# Шаг 1: Создание абстрактного класса Weapon
class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

# Шаг 2: Реализация конкретных типов оружия
class Sword(Weapon):
    def attack(self):
        return "Боец наносит удар мечом."

class Bow(Weapon):
    def attack(self):
        return "Боец стреляет из лука."

# Шаг 3: Модификация класса Fighter
class Fighter:
    def __init__(self, name):
        self.name = name
        self.weapon = None

    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def attack_monster(self, monster):
        if self.weapon:
            print(self.weapon.attack())
            damage = random.randint(1, 10)  # Симуляция урона
            monster.take_damage(damage)
            if monster.is_defeated():
                print("Монстр побежден!")
            else:
                print(f"Монстр остался в живых с {monster.health} здоровья.")
        else:
            print("У бойца нет оружия!")

# Класс Monster
class Monster:
    def __init__(self, health):
        self.health = health

    def take_damage(self, damage):
        self.health -= damage

    def is_defeated(self):
        return self.health <= 0

# Шаг 4: Реализация боя
def main():
    # Создаем бойца и монстра
    fighter = Fighter("Воин")
    monster = Monster(20)

    # Боец выбирает меч
    fighter.change_weapon(Sword())
    print(f"{fighter.name} выбирает меч.")
    fighter.attack_monster(monster)

    # Боец выбирает лук
    fighter.change_weapon(Bow())
    print(f"{fighter.name} выбирает лук.")
    fighter.attack_monster(monster)

if __name__ == "__main__":
    main()