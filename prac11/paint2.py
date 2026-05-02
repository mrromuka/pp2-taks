import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [
    (0,0,0),(255,0,0),(0,255,0),(0,0,255),
    (255,255,0),(255,165,0),(128,0,128),(0,255,255)
]

current_color = BLACK
tool = "brush"

drawing = False
start_pos = None

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

def draw_palette():
    for i, c in enumerate(colors):
        pygame.draw.rect(screen, c, (10 + i*40, 10, 30, 30))

def get_color(pos):
    x, y = pos
    for i, c in enumerate(colors):
        rect = pygame.Rect(10 + i*40, 10, 30, 30)
        if rect.collidepoint(x, y):
            return c
    return None

def draw_square(surf, color, start, end):
    size = max(abs(end[0]-start[0]), abs(end[1]-start[1]))
    rect = pygame.Rect(start[0], start[1], size, size)
    pygame.draw.rect(surf, color, rect, 2)

def draw_right_triangle(surf, color, start, end):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surf, color, points, 2)

def draw_equilateral_triangle(surf, color, start, end):
    side = abs(end[0]-start[0])
    height = side * math.sqrt(3) / 2
    p1 = (start[0], start[1])
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side/2, start[1] - height)
    pygame.draw.polygon(surf, color, [p1, p2, p3], 2)

def draw_rhombus(surf, color, start, end):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    dx = abs(end[0] - start[0]) // 2
    dy = abs(end[1] - start[1]) // 2
    points = [(cx, cy-dy), (cx+dx, cy), (cx, cy+dy), (cx-dx, cy)]
    pygame.draw.polygon(surf, color, points, 2)

while True:
    screen.fill(WHITE)
    screen.blit(canvas, (0,0))
    draw_palette()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: tool = "brush"
            if event.key == pygame.K_2: tool = "rect"
            if event.key == pygame.K_3: tool = "circle"
            if event.key == pygame.K_4: tool = "eraser"
            if event.key == pygame.K_5: tool = "square"
            if event.key == pygame.K_6: tool = "rtriangle"
            if event.key == pygame.K_7: tool = "etriangle"
            if event.key == pygame.K_8: tool = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            color = get_color(event.pos)
            if color:
                current_color = color
            else:
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                if tool == "rect":
                    rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif tool == "circle":
                    radius = int(math.hypot(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
                elif tool == "square":
                    draw_square(canvas, current_color, start_pos, end_pos)
                elif tool == "rtriangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos)
                elif tool == "etriangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos)
                elif tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos)
                drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "brush":
                    pygame.draw.circle(canvas, current_color, event.pos, 3)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, event.pos, 10)

    pygame.display.flip()
    clock.tick(60)