import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

snake = [(100, 100)]
direction = (CELL, 0)

foods = []

score = 0
level = 1
speed = 7

def spawn_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            weight = random.choice([1, 2, 3])
            lifetime = random.randint(3000, 7000)
            foods.append({
                "pos": (x, y),
                "weight": weight,
                "spawn": pygame.time.get_ticks(),
                "life": lifetime
            })
            break

for _ in range(3):
    spawn_food()

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, CELL):
        direction = (0, -CELL)
    if keys[pygame.K_DOWN] and direction != (0, -CELL):
        direction = (0, CELL)
    if keys[pygame.K_LEFT] and direction != (CELL, 0):
        direction = (-CELL, 0)
    if keys[pygame.K_RIGHT] and direction != (-CELL, 0):
        direction = (CELL, 0)

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        running = False

    if head in snake:
        running = False

    snake.insert(0, head)

    current_time = pygame.time.get_ticks()
    foods = [f for f in foods if current_time - f["spawn"] < f["life"]]

    for f in foods:
        if head == f["pos"]:
            score += f["weight"]
            for _ in range(f["weight"]):
                snake.append(snake[-1])
            foods.remove(f)
            spawn_food()
            break
    else:
        snake.pop()

    if score >= level * 4:
        level += 1
        speed += 2

    if len(foods) < 3:
        spawn_food()

    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL, CELL))

    for f in foods:
        color = (255, 0, 0) if f["weight"] == 1 else (255, 165, 0) if f["weight"] == 2 else (255, 255, 0)
        pygame.draw.rect(screen, color, (*f["pos"], CELL, CELL))

    text = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()