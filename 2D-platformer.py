import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Физика
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_FORCE = -15

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
PLATFORM_COLOR = (100, 100, 100)
COIN_COLOR = (255, 215, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Платформер")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont("Arial", 30)

### Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
        self.score = 0

    def update(self, platforms, coins):
        dx = 0
        dy = 0

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_SPACE] and not self.jumped and not self.in_air:
            self.vel_y = JUMP_FORCE
            self.jumped = True
        if not keys[pygame.K_SPACE]:
            self.jumped = False

        # Гравитация
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Проверка столкновений с платформами
        self.in_air = True
        for platform in platforms:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:  # Удар головой
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:  # Приземление
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        # Сбор монет
        for coin in coins[:]:
            if self.rect.colliderect(coin.rect):
                coins.remove(coin)
                self.score += 1

        # Обновление позиции
        self.rect.x += dx
        self.rect.y += dy

        # Границы экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.in_air = False

        return False  # False = игрок жив

### Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

### Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, COIN_COLOR, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

### Класс уровня
class Level:
    def __init__(self, level_num):
        self.platforms = []
        self.coins = []
        self.level_num = level_num
        self.generate_level()

    def generate_level(self):
        # Основная платформа (пол)
        ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
        self.platforms.append(ground)

        # Платформы в зависимости от уровня
        platform_count = 5 + self.level_num * 2
        for _ in range(platform_count):
            width = random.randint(50, 150)
            height = 20
            x = random.randint(0, SCREEN_WIDTH - width)
            y = random.randint(100, SCREEN_HEIGHT - 150)
            self.platforms.append(Platform(x, y, width, height))

            # Монеты над платформами
            if random.random() > 0.5:
                self.coins.append(Coin(x + width // 2, y - 30))

        # Дополнительные монеты
        for _ in range(3 + self.level_num):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.coins.append(Coin(x, y))

### Основная функция игры
def main():
    player = Player(100, SCREEN_HEIGHT - 100)
    levels = [Level(i) for i in range(3)]  # 3 уровня
    current_level = 0
    level = levels[current_level]

    game_over = False
    paused = False
    running = True

    while running:
        clock.tick(FPS)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if event.key == pygame.K_r and (game_over or len(level.coins) == 0):
                    # Рестарт
                    player = Player(100, SCREEN_HEIGHT - 100)
                    levels = [Level(i) for i in range(3)]
                    current_level = 0
                    level = levels[current_level]
                    game_over = False

        if not paused and not game_over:
            # Обновление игрока
            game_over = player.update(level.platforms, level.coins)

            # Переход на следующий уровень
            if len(level.coins) == 0:
                current_level += 1
                if current_level < len(levels):
                    level = levels[current_level]
                    player.rect.x = 100
                    player.rect.y = SCREEN_HEIGHT - 100
                else:
                    game_over = True  # Все уровни пройдены

        # Отрисовка
        screen.fill(SKY_BLUE)

        # Платформы
        for platform in level.platforms:
            screen.blit(platform.image, platform.rect)

        # Монеты
        for coin in level.coins:
            screen.blit(coin.image, coin.rect)

        # Игрок
        screen.blit(player.image, player.rect)

        # Интерфейс
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 80))
        draw_text(f"Уровень: {current_level + 1}", font, WHITE, 20, 20)
        draw_text(f"Монеты: {player.score}", font, WHITE, 20, 50)

        if paused:
            draw_text("ПАУЗА", font, WHITE, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)

        if game_over and current_level >= len(levels) - 1 and len(level.coins) == 0:
            draw_text("ПОБЕДА!", font, GREEN, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2)
            draw_text("Нажмите R для рестарта", font, WHITE, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40)

        pygame.display.update()

    pygame.quit()
    sys.exit()

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

if __name__ == "__main__":
    main()

