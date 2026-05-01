import pygame
import sys

from Ui import Button, draw_text
from Persistence import load_settings, save_settings, load_leaderboard
from racer import run_game, WIDTH, HEIGHT


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")

font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (30, 30, 30)


def get_username():
    name = ""
    active = True
    while active:
        screen.fill(BG)
        draw_text(screen, "Enter Username", font, WHITE, WIDTH // 2, 180, center=True)
        pygame.draw.rect(screen, WHITE, (90, 260, 300, 50), 2)
        draw_text(screen, name, font, WHITE, 105, 270)
        draw_text(screen, "Press ENTER to continue", small_font, WHITE, WIDTH // 2, 350, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12 and event.unicode.isprintable():
                        name += event.unicode

        pygame.display.flip()


def main_menu(settings):
    play_btn = Button(140, 180, 200, 50, "Play")
    leaderboard_btn = Button(140, 260, 200, 50, "Leaderboard")
    settings_btn = Button(140, 340, 200, 50, "Settings")
    quit_btn = Button(140, 420, 200, 50, "Quit")

    while True:
        screen.fill(BG)
        draw_text(screen, "Racer Game", font, WHITE, WIDTH // 2, 90, center=True)

        for btn in [play_btn, leaderboard_btn, settings_btn, quit_btn]:
            btn.draw(screen, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play_btn.is_clicked(event):
                username = get_username()
                result = run_game(screen, username, settings)
                if result["action"] == "quit":
                    pygame.quit()
                    sys.exit()
                game_over_screen(result, settings)

            if leaderboard_btn.is_clicked(event):
                leaderboard_screen()

            if settings_btn.is_clicked(event):
                settings_screen(settings)

            if quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()


def leaderboard_screen():
    back_btn = Button(160, 620, 160, 45, "Back")

    while True:
        screen.fill(BG)
        draw_text(screen, "Top 10 Leaderboard", font, WHITE, WIDTH // 2, 50, center=True)

        leaderboard = load_leaderboard()

        y = 120
        if not leaderboard:
            draw_text(screen, "No scores yet", small_font, WHITE, WIDTH // 2, 200, center=True)
        else:
            for i, entry in enumerate(leaderboard, start=1):
                text = f"{i}. {entry['name']} | Score: {entry['score']} | Dist: {entry['distance']}"
                draw_text(screen, text, small_font, WHITE, 25, y)
                y += 40

        back_btn.draw(screen, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                return

        pygame.display.flip()


def settings_screen(settings):
    back_btn = Button(160, 620, 160, 45, "Back")
    sound_btn = Button(140, 180, 200, 45, f"Sound: {'On' if settings['sound'] else 'Off'}")
    color_btn = Button(140, 270, 200, 45, f"Car: {settings['car_color']}")
    difficulty_btn = Button(140, 360, 200, 45, f"Difficulty: {settings['difficulty']}")

    colors = ["red", "blue", "yellow", "white"]
    difficulties = ["easy", "medium", "hard"]

    while True:
        screen.fill(BG)
        draw_text(screen, "Settings", font, WHITE, WIDTH // 2, 80, center=True)

        sound_btn.text = f"Sound: {'On' if settings['sound'] else 'Off'}"
        color_btn.text = f"Car: {settings['car_color']}"
        difficulty_btn.text = f"Difficulty: {settings['difficulty']}"

        sound_btn.draw(screen, small_font)
        color_btn.draw(screen, small_font)
        difficulty_btn.draw(screen, small_font)
        back_btn.draw(screen, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if sound_btn.is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color_btn.is_clicked(event):
                current_index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(current_index + 1) % len(colors)]
                save_settings(settings)

            if difficulty_btn.is_clicked(event):
                current_index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(current_index + 1) % len(difficulties)]
                save_settings(settings)

            if back_btn.is_clicked(event):
                return

        pygame.display.flip()


def game_over_screen(result, settings):
    retry_btn = Button(140, 420, 200, 45, "Retry")
    menu_btn = Button(140, 490, 200, 45, "Main Menu")

    while True:
        screen.fill(BG)
        draw_text(screen, "Game Over", font, WHITE, WIDTH // 2, 100, center=True)
        draw_text(screen, f"Score: {result['score']}", small_font, WHITE, WIDTH // 2, 200, center=True)
        draw_text(screen, f"Distance: {result['distance']}", small_font, WHITE, WIDTH // 2, 240, center=True)
        draw_text(screen, f"Coins: {result['coins']}", small_font, WHITE, WIDTH // 2, 280, center=True)

        retry_btn.draw(screen, small_font)
        menu_btn.draw(screen, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry_btn.is_clicked(event):
                username = get_username()
                result = run_game(screen, username, settings)
                if result["action"] == "quit":
                    pygame.quit()
                    sys.exit()

            if menu_btn.is_clicked(event):
                return

        pygame.display.flip()


def main():
    settings = load_settings()
    main_menu(settings)


if __name__ == "__main__":
    main()