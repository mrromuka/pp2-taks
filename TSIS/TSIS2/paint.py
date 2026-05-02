import pygame
import sys
from collections import deque
from datetime import datetime

pygame.init()


WIDTH, HEIGHT = 1200, 800
TOOLBAR_HEIGHT = 100
CANVAS_RECT = pygame.Rect(0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
BROWN = (139, 69, 19)

COLOR_OPTIONS = [
    BLACK, WHITE, RED, GREEN, BLUE,
    YELLOW, PURPLE, ORANGE, PINK, BROWN
]


font = pygame.font.SysFont("arial", 20)
small_font = pygame.font.SysFont("arial", 16)


canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)


TOOLS = [
    "pencil", "line", "rect", "circle", "square",
    "right_triangle", "equilateral_triangle", "rhombus",
    "eraser", "fill", "text", "picker"
]

current_tool = "pencil"
current_color = BLACK
brush_size = 2

BRUSH_SIZES = {
    1: 2,
    2: 5,
    3: 10
}


drawing = False
start_pos = None
last_pos = None
current_pos = None

text_mode = False
text_position = None
text_input = ""


tool_buttons = {}
color_buttons = []
size_buttons = {}

tool_x = 10
tool_y = 10
tool_w = 100
tool_h = 30
gap = 10

for i, tool in enumerate(TOOLS):
    row = i // 6
    col = i % 6
    rect = pygame.Rect(tool_x + col * (tool_w + gap), tool_y + row * (tool_h + gap), tool_w, tool_h)
    tool_buttons[tool] = rect

color_x = 700
color_y = 10
color_size = 30

for i, color in enumerate(COLOR_OPTIONS):
    rect = pygame.Rect(color_x + (i % 5) * 40, color_y + (i // 5) * 40, color_size, color_size)
    color_buttons.append((rect, color))

size_buttons[1] = pygame.Rect(950, 10, 60, 30)
size_buttons[2] = pygame.Rect(1020, 10, 60, 30)
size_buttons[3] = pygame.Rect(1090, 10, 60, 30)


def draw_toolbar():
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))


    for tool, rect in tool_buttons.items():
        color = DARK_GRAY if tool == current_tool else GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        label = small_font.render(tool, True, BLACK)
        screen.blit(label, (rect.x + 5, rect.y + 7))


    for rect, color in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if color == current_color:
            pygame.draw.rect(screen, BLACK, rect, 4)

    
    for key, rect in size_buttons.items():
        color = DARK_GRAY if BRUSH_SIZES[key] == brush_size else GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        label = font.render(str(key), True, BLACK)
        screen.blit(label, (rect.x + 22, rect.y + 4))


    info_text = font.render(
        f"Tool: {current_tool} | Color: {current_color} | Brush: {brush_size}px | Ctrl+S to save",
        True,
        BLACK
    )
    screen.blit(info_text, (10, 75))


def draw_on_screen():
    screen.fill(WHITE)
    draw_toolbar()
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))


    if drawing and start_pos and current_pos and current_tool in [
        "line", "rect", "circle", "square",
        "right_triangle", "equilateral_triangle", "rhombus"
    ]:
        preview = canvas.copy()
        draw_shape(preview, current_tool, start_pos, current_pos, current_color, brush_size)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_mode and text_position:
        preview_text = font.render(text_input, True, current_color)
        screen.blit(preview_text, text_position)

    pygame.display.flip()


def canvas_mouse_pos(pos):
    return (pos[0], pos[1] - TOOLBAR_HEIGHT)


def inside_canvas(screen_pos):
    return CANVAS_RECT.collidepoint(screen_pos)


def save_canvas():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved as {filename}")


def draw_shape(surface, tool, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    if tool == "line":
        pygame.draw.line(surface, color, start, end, width)

    elif tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, width)

    elif tool == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, width)

    elif tool == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        x = x1 if x2 >= x1 else x1 - side
        y = y1 if y2 >= y1 else y1 - side
        rect = pygame.Rect(x, y, side, side)
        pygame.draw.rect(surface, color, rect, width)

    
    elif tool == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "equilateral_triangle":
        dx = x2 - x1
        side = abs(dx)
        height = int((3 ** 0.5 / 2) * side)
        if y2 >= y1:
            points = [(x1, y1), (x1 - side // 2, y1 + height), (x1 + side // 2, y1 + height)]
        else:
            points = [(x1, y1), (x1 - side // 2, y1 - height), (x1 + side // 2, y1 - height)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color):
    w, h = surface.get_size()
    x, y = start_pos

    if not (0 <= x < w and 0 <= y < h):
        return

    target_color = surface.get_at((x, y))
    fill_color_rgba = pygame.Color(*fill_color)

    if target_color == fill_color_rgba:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= w or py < 0 or py >= h:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))



clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = BRUSH_SIZES[1]
            elif event.key == pygame.K_2:
                brush_size = BRUSH_SIZES[2]
            elif event.key == pygame.K_3:
                brush_size = BRUSH_SIZES[3]

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            if text_mode:
                if event.key == pygame.K_RETURN:
                    if text_input and text_position:
                        rendered = font.render(text_input, True, current_color)
                        canvas.blit(rendered, (text_position[0], text_position[1] - TOOLBAR_HEIGHT))
                    text_mode = False
                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

         
            clicked_toolbar = False

            for tool, rect in tool_buttons.items():
                if rect.collidepoint(mouse_pos):
                    current_tool = tool
                    clicked_toolbar = True
                    text_mode = False
                    break

            for rect, color in color_buttons:
                if rect.collidepoint(mouse_pos):
                    current_color = color
                    clicked_toolbar = True
                    break

            for key, rect in size_buttons.items():
                if rect.collidepoint(mouse_pos):
                    brush_size = BRUSH_SIZES[key]
                    clicked_toolbar = True
                    break

            if clicked_toolbar:
                continue

            if inside_canvas(mouse_pos):
                cpos = canvas_mouse_pos(mouse_pos)

                if current_tool == "picker":
                    current_color = canvas.get_at(cpos)[:3]

                elif current_tool == "fill":
                    flood_fill(canvas, cpos, current_color)

                elif current_tool == "text":
                    text_mode = True
                    text_position = mouse_pos
                    text_input = ""

                else:
                    drawing = True
                    start_pos = cpos
                    current_pos = cpos
                    last_pos = cpos

                    if current_tool == "pencil":
                        pygame.draw.circle(canvas, current_color, cpos, brush_size // 2 + 1)

                    elif current_tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, cpos, brush_size // 2 + 3)

   
        elif event.type == pygame.MOUSEMOTION:
            if drawing and inside_canvas(event.pos):
                cpos = canvas_mouse_pos(event.pos)
                current_pos = cpos

                if current_tool == "pencil" and last_pos:
                    pygame.draw.line(canvas, current_color, last_pos, cpos, brush_size)
                    last_pos = cpos

                elif current_tool == "eraser" and last_pos:
                    pygame.draw.line(canvas, WHITE, last_pos, cpos, brush_size + 6)
                    last_pos = cpos


        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if inside_canvas(event.pos):
                    end_pos = canvas_mouse_pos(event.pos)
                else:
                    end_pos = current_pos

                if current_tool in [
                    "line", "rect", "circle", "square",
                    "right_triangle", "equilateral_triangle", "rhombus"
                ]:
                    draw_shape(canvas, current_tool, start_pos, end_pos, current_color, brush_size)

                drawing = False
                start_pos = None
                current_pos = None
                last_pos = None

    draw_on_screen()
    clock.tick(60)