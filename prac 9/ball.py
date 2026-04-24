import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")


WHITE = (255, 255, 255)
RED = (255, 0, 0)


radius = 25
x, y = WIDTH // 2, HEIGHT // 2
speed = 20

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x - speed - radius >= 0:
                    x -= speed

            if event.key == pygame.K_RIGHT:
                if x + speed + radius <= WIDTH:
                    x += speed

            if event.key == pygame.K_UP:
                if y - speed - radius >= 0:
                    y -= speed

            if event.key == pygame.K_DOWN:
                if y + speed + radius <= HEIGHT:
                    y += speed


    screen.fill(WHITE)


    pygame.draw.circle(screen, RED, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)