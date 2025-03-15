import pygame
import time
import math

pygame.init()

WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

background = pygame.image.load("mickey_face.jpeg")
minute_hand = pygame.image.load("right_hand-removebg-preview.png")
second_hand = pygame.image.load("left_hand-removebg-preview.png")

background = pygame.transform.scale(background, (WIDTH, HEIGHT))
minute_hand = pygame.transform.scale(minute_hand, (250, 200))
second_hand = pygame.transform.scale(second_hand, (350, 300))

center_x, center_y = WIDTH // 2, HEIGHT // 2

running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    minute_angle = -minutes * 6
    second_angle = -seconds * 6

    rotated_minute_hand = pygame.transform.rotate(minute_hand, minute_angle)
    rotated_second_hand = pygame.transform.rotate(second_hand, second_angle)

    min_rect = rotated_minute_hand.get_rect(center=(center_x, center_y))
    sec_rect = rotated_second_hand.get_rect(center=(center_x, center_y))

    screen.blit(rotated_minute_hand, min_rect.topleft)
    screen.blit(rotated_second_hand, sec_rect.topleft)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.time.delay(1000)

pygame.quit()
