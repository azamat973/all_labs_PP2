import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Red Ball")

RADIUS = 25
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
SPEED = 20

running = True
while running:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ball_x - RADIUS - SPEED >= 0:
        ball_x -= SPEED
    if keys[pygame.K_RIGHT] and ball_x + RADIUS + SPEED <= WIDTH:
        ball_x += SPEED
    if keys[pygame.K_UP] and ball_y - RADIUS - SPEED >= 0:
        ball_y -= SPEED
    if keys[pygame.K_DOWN] and ball_y + RADIUS + SPEED <= HEIGHT:
        ball_y += SPEED

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (ball_x, ball_y), RADIUS)
    pygame.display.update()

pygame.quit()