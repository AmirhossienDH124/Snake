import pygame
import sys
import random

pygame.init()

width = 12*32
height = 12*32
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Snake")

pygame.mouse.set_visible(False)

fps_clock = pygame.time.Clock()

all_pos = []
all_dir = []

snake_image = pygame.Surface((32, 32))
snake_image.fill((192, 192, 192))
snake_pos = [96, 96]
snake_direction = [0, 32]

body_image = pygame.Surface((32, 32))
body_image.fill((128, 128, 128))

apple_image = pygame.Surface((32, 32))
apple_image.fill((170, 0, 0))
apple_pos = [random.randint(0, width - 32) // 32 * 32, random.randint(0, height - 32) // 32 * 32]

for i in range(2):
    all_pos.append([96, 96-(i+1)*32])
    all_dir.append([0, 32])


def game_over():
    body_number = len(all_pos)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
        # screen.fill((170, 170, 170), (width//2-128, height//2-32, width-128, 64))
        font = pygame.font.Font(pygame.font.get_default_font(), 32)
        text_surface = font.render(f"RECORD: {body_number}", True, (255, 255, 255), (128, 128, 128))
        screen.blit(text_surface, ((width-text_surface.get_width())//2, (height-text_surface.get_height())//2))
        pygame.display.update()
        fps_clock.tick(2)


while True:
    all_dir.insert(0, [snake_direction[0], snake_direction[1]])
    all_dir.pop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if abs(snake_direction[1]) > 0:
                if event.key == pygame.K_LEFT:
                    snake_direction = [-32, 0]
                if event.key == pygame.K_RIGHT:
                    snake_direction = [32, 0]
            if abs(snake_direction[0]) > 0:
                if event.key == pygame.K_UP:
                    snake_direction = [0, -32]
                if event.key == pygame.K_DOWN:
                    snake_direction = [0, 32]

    screen.fill((0, 0, 0))
    
    # Move
    snake_pos[0] += snake_direction[0]
    snake_pos[1] += snake_direction[1]
    for index, pos in enumerate(all_pos):
        pos[0] += all_dir[index][0]
        pos[1] += all_dir[index][1]
        # Game Over
        if pygame.Rect(snake_pos[0], snake_pos[1], 32, 32).colliderect(pygame.Rect(pos[0], pos[1], 32, 32)):
            game_over()

    # Game Over
    if snake_pos[0] < 0 or snake_pos[0] + 32 > width or snake_pos[1] < 0 or snake_pos[1] + 32 > height:
        game_over()

    # Collision
    if pygame.Rect(snake_pos[0], snake_pos[1], 32, 32).colliderect(pygame.Rect(apple_pos[0], apple_pos[1], 32, 32)):
        for index, pos in enumerate(all_pos):
            pos[0] -= all_dir[index][0]
            pos[1] -= all_dir[index][1]
        all_pos.insert(0, [snake_pos[0] - snake_direction[0], snake_pos[1] - snake_direction[1]])
        all_dir.append(snake_direction)
        apple_pos[0] = random.randint(0, width - 32) // 32 * 32
        apple_pos[1] = random.randint(0, height - 32) // 32 * 32
    
    # Draw
    screen.blit(snake_image, snake_pos)
    for pos in all_pos:
        screen.blit(body_image, pos)
    screen.blit(apple_image, apple_pos)

    pygame.display.update()
    fps_clock.tick(2)
