import pygame
import sys

pygame.init()

W, H = 900, 650
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)

colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0)]
color_names = ["Black", "Red", "Green", "Blue", "Yellow"]

font = pygame.font.Font(None, 24)

tool = "pen"
color = BLACK

drawing = False
start_pos = None

canvas_rect = pygame.Rect(0, 80, W, H-80)

screen.fill(WHITE)

def draw_ui():
    pygame.draw.rect(screen, GRAY, (0, 0, W, 80))

    # tools
    tools = ["Pen", "Eraser", "Rect", "Circle"]
    for i, t in enumerate(tools):
        r = pygame.Rect(10 + i*110, 10, 100, 30)
        pygame.draw.rect(screen, (180,180,180), r)
        text = font.render(t, True, BLACK)
        screen.blit(text, (r.x + 10, r.y + 7))

    # colors
    for i, c in enumerate(colors):
        r = pygame.Rect(10 + i*60, 45, 40, 25)
        pygame.draw.rect(screen, c, r)
        if c == color:
            pygame.draw.rect(screen, BLACK, r, 2)

def get_click(mx, my):
    if my < 40:
        if 10 <= mx <= 110: return ("tool", "pen")
        if 120 <= mx <= 220: return ("tool", "eraser")
        if 230 <= mx <= 330: return ("tool", "rect")
        if 340 <= mx <= 440: return ("tool", "circle")

    if 45 <= my <= 70:
        for i in range(len(colors)):
            if 10 + i*60 <= mx <= 50 + i*60:
                return ("color", colors[i])

    return (None, None)

while True:
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            kind, val = get_click(mx, my)
            if kind == "tool":
                tool = val
                continue
            if kind == "color":
                color = val
                continue

            if canvas_rect.collidepoint(mx, my):
                drawing = True
                start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                end_pos = event.pos

                if tool == "rect":
                    x1,y1 = start_pos
                    x2,y2 = end_pos
                    pygame.draw.rect(screen, color,
                        (min(x1,x2), min(y1,y2), abs(x1-x2), abs(y1-y2)))

                elif tool == "circle":
                    x1,y1 = start_pos
                    x2,y2 = end_pos
                    r = int(((x2-x1)**2 + (y2-y1)**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, r)

            drawing = False
            start_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            if canvas_rect.collidepoint(event.pos):
                if tool == "pen":
                    pygame.draw.circle(screen, color, event.pos, 3)
                elif tool == "eraser":
                    pygame.draw.circle(screen, WHITE, event.pos, 10)

    pygame.display.update()