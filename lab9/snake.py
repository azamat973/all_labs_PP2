import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы экрана
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SCORE_TO_LEVEL_UP = 5  # Количество очков для повышения уровня
FOOD_LIFETIME = 5000  # Время жизни еды в миллисекундах (5 секунд)

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Шрифт
font = pygame.font.Font(None, 30)


def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def generate_food():
    return (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE), pygame.time.get_ticks()


def game_over_screen():
    screen.fill(RED)
    draw_text("Game Over", 50, WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 50)
    draw_text("Press SPACE to Restart", 30, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 20)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Начальные параметры игры
snake = [(WIDTH // 2, HEIGHT // 2)]
snake_dir = (GRID_SIZE, 0)
food, food_spawn_time = generate_food()
food_weight = random.choice([1, 2, 3])
score = 0
level = 1
running = True

game_over = False
FPS = 60  # Фиксированный FPS
clock = pygame.time.Clock()
last_move_time = 0
MOVE_DELAY = 100  # Интервал в миллисекундах (чем меньше, тем быстрее змейка)

# Основной игровой цикл
while running:
    if game_over:
        game_over_screen()
        # Сброс параметров игры
        snake = [(WIDTH // 2, HEIGHT // 2)]
        snake_dir = (GRID_SIZE, 0)
        food, food_spawn_time = generate_food()
        score = 0
        level = 1
        MOVE_DELAY = 100
        game_over = False

    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, GRID_SIZE):
                snake_dir = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -GRID_SIZE):
                snake_dir = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (GRID_SIZE, 0):
                snake_dir = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-GRID_SIZE, 0):
                snake_dir = (GRID_SIZE, 0)

    # Проверка времени жизни еды
    if current_time - food_spawn_time > FOOD_LIFETIME:
        food, food_spawn_time = generate_food()
        food_weight = random.choice([1, 2, 3])

    # Двигаем змейку с фиксированным интервалом времени
    if current_time - last_move_time > MOVE_DELAY:
        last_move_time = current_time
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)

        if new_head in snake:
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += food_weight
                food, food_spawn_time = generate_food()
                food_weight = random.choice([1, 2, 3])
                if score % SCORE_TO_LEVEL_UP == 0:
                    level += 1
                    MOVE_DELAY = max(50, MOVE_DELAY - 5)  # Уменьшаем задержку (ускоряем змейку)
            else:
                snake.pop()

    # Отрисовка змейки
    pygame.draw.rect(screen, DARK_GREEN, (snake[0][0], snake[0][1], GRID_SIZE, GRID_SIZE))
    for segment in snake[1:]:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    # Отрисовка еды
    food_color = RED if food_weight == 1 else BLUE if food_weight == 2 else WHITE
    pygame.draw.rect(screen, food_color, (food[0], food[1], GRID_SIZE, GRID_SIZE))

    # Отображение очков и уровня
    draw_text(f"Score: {score}", 30, WHITE, 70, 15)
    draw_text(f"Level: {level}", 30, WHITE, 70, 45)

    pygame.display.flip()
    clock.tick(FPS)  # Фиксированный FPS (60)

pygame.quit()