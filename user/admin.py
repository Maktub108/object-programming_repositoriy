class User:
    def __init__(self, user_id, name):
        self.__user_id = user_id         # Уникальный идентификатор
        self.__name = name               # Имя пользователя
        self.__access_level = 'user'     # Уровень доступа

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_access_level(self):
        return self.__access_level

    def set_name(self, name):
        self.__name = name


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.__access_level = 'admin'  # Уровень доступа для администраторов

    def add_user(self, user_list, user_id, name):
        new_user = User(user_id, name)
        user_list.append(new_user)
        print(f"Пользователь {name} добавлен.")

    def remove_user(self, user_list, user_id):
        for user in user_list:
            if user.get_user_id() == user_id:
                user_list.remove(user)
                print(f"Пользователь {user.get_name()} удален.")
                return
        print("Пользователь не найден.")


# Пример использования
if __name__ == "__main__":
    user_list = []

    admin = Admin(user_id=1, name="Admin User")
    admin.add_user(user_list, user_id=2, name="Konstantin ")
    admin.add_user(user_list, user_id=3, name="Victoria")

    print("Список пользователей:")
    for user in user_list:
        print(f"ID: {user.get_user_id()}, Name: {user.get_name()}, Access Level: {user.get_access_level()}")

    admin.remove_user(user_list, user_id=2)

    print("Список пользователей после удаления:")
    for user in user_list:
        print(f"ID: {user.get_user_id()}, Name: {user.get_name()}, Access Level: {user.get_access_level()}")
