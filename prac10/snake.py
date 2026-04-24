import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

color = BLACK
tool = "brush"
start_pos = None

screen.fill(WHITE)

def draw_ui():
    pygame.draw.rect(screen, RED, (0, 0, 50, 50))
    pygame.draw.rect(screen, GREEN, (50, 0, 50, 50))
    pygame.draw.rect(screen, BLUE, (100, 0, 50, 50))
    pygame.draw.rect(screen, BLACK, (150, 0, 50, 50))

    pygame.draw.rect(screen, (200,200,200), (200,0,100,50))
    pygame.draw.rect(screen, (200,200,200), (300,0,100,50))
    pygame.draw.rect(screen, (200,200,200), (400,0,100,50))

    font = pygame.font.Font(None, 24)
    screen.blit(font.render("Brush", True, BLACK), (210, 15))
    screen.blit(font.render("Rect", True, BLACK), (310, 15))
    screen.blit(font.render("Circle", True, BLACK), (410, 15))

def get_color(pos):
    x, y = pos
    if y < 50:
        if x < 50: return RED
        if x < 100: return GREEN
        if x < 150: return BLUE
        if x < 200: return BLACK
    return None

running = True

while running:
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            new_color = get_color(pos)
            if new_color:
                color = new_color
                continue

            if 200 <= pos[0] <= 300:
                tool = "brush"
            elif 300 <= pos[0] <= 400:
                tool = "rect"
                start_pos = pos
            elif 400 <= pos[0] <= 500:
                tool = "circle"
                start_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                x, y = event.pos

                if tool == "brush":
                    pygame.draw.circle(screen, color, (x, y), 5)

                elif tool == "eraser":
                    pygame.draw.circle(screen, WHITE, (x, y), 10)

        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = pygame.mouse.get_pos()

            if tool == "rect" and start_pos:
                x1, y1 = start_pos
                x2, y2 = end_pos
                pygame.draw.rect(screen, color, (min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2)))

            if tool == "circle" and start_pos:
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(math.hypot(x2-x1, y2-y1))
                pygame.draw.circle(screen, color, start_pos, radius)

            start_pos = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()