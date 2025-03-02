import pygame
import random

pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
ENEMY_SPAWN_RATE = 30  # чем меньше число, тем чаще появляются враги
FPS = 60

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Класс Игрок
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        # Ограничиваем движение игрока в пределах окна
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# Класс Враг
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - ENEMY_SIZE), 0, ENEMY_SIZE, ENEMY_SIZE)

    def move(self):
        self.rect.y += 5  # скорость движения врага

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Основная игра
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Игра на выживание")
    clock = pygame.time.Clock()

    player = Player()
    enemies = []
    score = 0
    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_UP]:
            dy = -5
        if keys[pygame.K_DOWN]:
            dy = 5

        player.move(dx, dy)

        # Появление врагов
        if random.randint(1, ENEMY_SPAWN_RATE) == 1:
            enemies.append(Enemy())

        # Движение врагов и удаление вышедших за пределы экрана
        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.y > HEIGHT:  # Удаляем врагов, вышедших за пределы экрана
                enemies.remove(enemy)
                score += 1

        # Проверка на столкновение
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                running = False  # Конец игры при столкновении

        # Отрисовка
        screen.fill(WHITE)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Обновление дисплея
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print(f"Игра закончена! Ваш результат: {score}")

if __name__ == "__main__":
    main()


