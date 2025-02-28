
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        raise NotImplementedError("Метод make_sound должен быть переопределен в подклассах.")

    def eat(self):
        print(f"{self.name} ест.")


# Подкласс Bird
class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.wing_span = wing_span

    def make_sound(self):
        return "Чирик!"


# Подкласс Mammal
class Mammal(Animal):
    def __init__(self, name, age, habitat):
        super().__init__(name, age)
        self.habitat = habitat

    def make_sound(self):
        return "Рррр!"


# Подкласс Reptile
class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        return "Шшш!"


# Функция для демонстрации полиморфизма
def animal_sound(animals):
    for animal in animals:
        print(f"{animal.name} говорит: {animal.make_sound()}")


# Класс Zoo
class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Животное {animal.name} добавлено в зоопарк.")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"Сотрудник {staff_member.name} добавлен в зоопарк.")


# Класс ZooKeeper
class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}.")


# Класс Veterinarian
class Veterinarian:
    def __init__(self, name):
        self.name = name

    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}.")


# Пример использования
if __name__ == "__main__":
    # Создаем животных
    parrot = Bird(name="Попугай", age=2, wing_span=15)
    lion = Mammal(name="Лев", age=5, habitat="Савана")
    snake = Reptile(name="Змея", age=3, scale_type="Чешуя")

    # Создаем зоопарк
    zoo = Zoo()
    zoo.add_animal(parrot)
    zoo.add_animal(lion)
    zoo.add_animal(snake)

    # Создаем сотрудников
    keeper = ZooKeeper(name="Джон")
    vet = Veterinarian(name="Доктор Смит")
    zoo.add_staff(keeper)
    zoo.add_staff(vet)

    # Демонстрируем полиморфизм
    animal_sound(zoo.animals)