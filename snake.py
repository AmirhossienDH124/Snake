import pygame
import sys
import random

pygame.init()

width = 12 * 32
height = 12 * 32
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Snake")
pygame.mouse.set_visible(False)

fps_clock = pygame.time.Clock()

all_pos = []
all_dir = []

snake_image = pygame.Surface((32, 32))
snake_image.fill((170, 170, 170))
snake_pos = [96, 96]
snake_dir = [32, 0]
speed = 32

body_number = 2
for b in range(body_number):
    all_pos.append([96 - (b + 1) * 32, 96])
    all_dir.append([32, 0])

body_image = pygame.Surface((32, 32))
body_image.fill((85, 85, 85))

apple_image = pygame.Surface((32, 32))
apple_image.fill((170, 0, 0))
apple_pos = [random.randint(0, width-32)//32*32, random.randint(0, height-32)//32*32]

while True:
    all_dir.insert(0, [snake_dir[0], snake_dir[1]])
    all_dir.pop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_LEFT:
                snake_dir[0] = -speed
                snake_dir[1] = 0
            if event.key == pygame.K_RIGHT:
                snake_dir[0] = speed
                snake_dir[1] = 0
            if event.key == pygame.K_UP:
                snake_dir[1] = -speed
                snake_dir[0] = 0
            if event.key == pygame.K_DOWN:
                snake_dir[1] = speed
                snake_dir[0] = 0

    screen.fill((0, 0, 0))

    # Update Position
    snake_pos[0] += snake_dir[0]
    snake_pos[1] += snake_dir[1]
    for index, pos in enumerate(all_pos):
        pos[0] += all_dir[index][0]
        pos[1] += all_dir[index][1]

    # Check Collision
    if pygame.Rect(snake_pos[0], snake_pos[1], 32, 32).colliderect(pygame.Rect(apple_pos[0], apple_pos[1], 32, 32)):
        body_number += 1
        for index, pos in enumerate(all_pos):
            pos[0] -= all_dir[index][0]
            pos[1] -= all_dir[index][1]
        all_pos.insert(0, [snake_pos[0] - snake_dir[0], snake_pos[1] - snake_dir[1]])
        all_dir.append(snake_dir)
        apple_pos[0] = random.randint(0, width - 32) // 32 * 32
        apple_pos[1] = random.randint(0, height - 32) // 32 * 32

    # Draw Objects
    screen.blit(snake_image, snake_pos)
    for pos in all_pos:
        screen.blit(body_image, pos)
    screen.blit(apple_image, apple_pos)

    pygame.display.update()
    fps_clock.tick(2)
