import pygame, sys, random, time, psycopg2
from pygame.locals import *
# -*- coding: utf-8 -*-

DB_NAME = "snake_game_db"
DB_USER = "postgres"
DB_PASSWORD = "kbtu.aza_007"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    return conn, cur

def create_users_tables():
    conn, cur = connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            score INTEGER,
            level INTEGER,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_user(username):
    conn, cur = connect_db()
    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    row = cur.fetchone()
    if row:
        user_id = row[0]
        print(f"User '{username}' found with id={user_id}.")
    else:
        cur.execute("INSERT INTO users(username) VALUES(%s) RETURNING id;", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        print(f"New user '{username}' created with id={user_id}.")
    cur.close()
    conn.close()
    return user_id

def get_last_state(user_id):
    conn, cur = connect_db()
    cur.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1;", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return row[0], row[1]
    return 0, 1

def save_state(user_id, score, level):
    conn, cur = connect_db()
    cur.execute("INSERT INTO user_score(user_id, score, level) VALUES(%s, %s, %s);", (user_id, score, level))
    conn.commit()
    cur.close()
    conn.close()
    print(f"State saved: score={score}, level={level}.")

create_users_tables()
username = input("Enter your username: ")
user_id = get_or_create_user(username)
last_score, last_level = get_last_state(user_id)
print(f"Welcome, {username}! Your last level was: {last_level}")

pygame.init()
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

screen.fill(BLACK)
ready_font = pygame.font.SysFont("Verdana", 40)
ready_text = ready_font.render("Get Ready...", True, WHITE)
screen.blit(ready_text, ((WIDTH - ready_text.get_width()) // 2, (HEIGHT - ready_text.get_height()) // 2))
pygame.display.update()
pygame.time.wait(5000)

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == QUIT:
            waiting = False
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_s:
                waiting = False
    screen.fill(BLACK)
    start_font = pygame.font.SysFont("Verdana", 40)
    start_text = start_font.render("Press S to start", True, WHITE)
    screen.blit(start_text, ((WIDTH - start_text.get_width()) // 2, (HEIGHT - start_text.get_height()) // 2))
    pygame.display.update()
    clock.tick(10)

def generate_food(snake):
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) not in snake:
            return (x, y)

def draw_snake(snake):
    for seg in snake:
        rect = pygame.Rect(seg[0] * CELL_SIZE, seg[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_food(food):
    rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)

def draw_info(score, level):
    font_info = pygame.font.SysFont("Verdana", 20)
    text = font_info.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

snake = [(COLS // 2, ROWS // 2)]
direction = (1, 0)
food = generate_food(snake)
score = 0
level = last_level
speed = 3 + (level - 1) * 2
foods_eaten = 0
paused = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = True
                while paused:
                    for pevent in pygame.event.get():
                        if pevent.type == QUIT:
                            paused = False
                            running = False
                        elif pevent.type == KEYDOWN:
                            paused = False
                    screen.fill(BLACK)
                    pause_font = pygame.font.SysFont("Verdana", 20)
                    pause_text = pause_font.render("Paused. Press any key to resume.", True, WHITE)
                    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
                    pygame.display.update()
                    clock.tick(5)
            else:
                if event.key == K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS or new_head in snake:
        save_state(user_id, score, level)
        running = False
    snake.insert(0, new_head)
    if new_head == food:
        score += 10
        foods_eaten += 1
        food = generate_food(snake)
        if foods_eaten % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food)
    draw_info(score, level)
    pygame.display.update()
    clock.tick(speed)

pygame.quit()
sys.exit()
