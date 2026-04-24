import pygame
import random

pygame.init()

w, h = 600, 400
cell = 10

screen = pygame.display.set_mode((w, h))

x, y = 300, 200
dx, dy = cell, 0

snake = [(x, y)]
length = 1

score = 0
level = 1

food = (0, 0)

clock = pygame.time.Clock()

def spawn_food():
    while True:
        fx = random.randrange(0, w, cell)
        fy = random.randrange(0, h, cell)
        if (fx, fy) not in snake:
            return (fx, fy)

food = spawn_food()

run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        dx, dy = -cell, 0
    if keys[pygame.K_RIGHT]:
        dx, dy = cell, 0
    if keys[pygame.K_UP]:
        dx, dy = 0, -cell
    if keys[pygame.K_DOWN]:
        dx, dy = 0, cell

    x += dx
    y += dy

    snake.append((x, y))

    if len(snake) > length:
        snake.pop(0)

    # wall collision
    if x < 0 or x >= w or y < 0 or y >= h:
        run = False

    # self collision
    if (x, y) in snake[:-1]:
        run = False

    # food collision
    if (x, y) == food:
        score += 1
        length += 1
        food = spawn_food()

        # level system
        if score % 3 == 0:
            level += 1

    # speed increases with level
    speed = 10 + level * 2

    screen.fill((0, 0, 0))

    # draw snake
    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (s[0], s[1], cell, cell))

    # draw food
    pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], cell, cell))

    # text (score + level)
    font = pygame.font.Font(None, 30)
    text = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()