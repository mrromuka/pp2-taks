import json
import os
import random
import pygame

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, FPS,
    BG_COLOR, TEXT_COLOR, FOOD_COLOR, POISON_COLOR, OBSTACLE_COLOR, FONT_NAME,
    MAIN_BG_PATH, GAME_OVER_BG_PATH, EAT_SOUND_PATH, DEATH_SOUND_PATH
)
import db

SETTINGS_FILE = "settings.json"

POWER_UPS = {
    "speed": {"color": (255, 215, 0), "duration": 5000},
    "slow": {"color": (80, 170, 255), "duration": 5000},
    "shield": {"color": (180, 120, 255), "duration": 0},
}


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface, font):
        pygame.draw.rect(surface, (55, 55, 55), self.rect, border_radius=10)
        pygame.draw.rect(surface, (180, 180, 180), self.rect, 2, border_radius=10)
        txt = font.render(self.text, True, TEXT_COLOR)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.audio_available = True
        try:
            pygame.mixer.init()
        except Exception:
            self.audio_available = False

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("TSIS 3 - Snake Game")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(FONT_NAME, 26)
        self.small_font = pygame.font.SysFont(FONT_NAME, 20)
        self.big_font = pygame.font.SysFont(FONT_NAME, 40)

        self.main_bg = self.load_background(MAIN_BG_PATH)
        self.game_over_bg = self.load_background(GAME_OVER_BG_PATH)

        self.eat_sound = self.load_sound(EAT_SOUND_PATH)
        self.death_sound = self.load_sound(DEATH_SOUND_PATH)

        self.settings = self.load_settings()
        self.username = ""
        self.personal_best = 0
        self.final_saved = False

        try:
            db.init_db()
            self.db_ready = True
        except Exception as e:
            self.db_ready = False
            print("DB init error:", e)

        self.state = "menu"
        self.menu_buttons = [
            Button((300, 220, 200, 45), "Play"),
            Button((300, 280, 200, 45), "Leaderboard"),
            Button((300, 340, 200, 45), "Settings"),
            Button((300, 400, 200, 45), "Quit"),
        ]
        self.game_over_buttons = [
            Button((300, 400, 200, 45), "Retry"),
            Button((300, 460, 200, 45), "Main Menu"),
        ]
        self.back_button = Button((20, 20, 110, 40), "Back")
        self.save_back_button = Button((300, 520, 200, 45), "Save & Back")
        self.color_buttons = [
            ((220, 370, 60, 40), (0, 255, 0)),
            ((300, 370, 60, 40), (255, 255, 0)),
            ((380, 370, 60, 40), (0, 200, 255)),
            ((460, 370, 60, 40), (255, 100, 100)),
            ((540, 370, 60, 40), (255, 255, 255)),
        ]

        self.reset_game()

    def load_background(self, path):
        if os.path.exists(path):
            image = pygame.image.load(path)
            return pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        return None

    def load_sound(self, path):
        if self.audio_available and os.path.exists(path):
            return pygame.mixer.Sound(path)
        return None

    def play_sound(self, sound):
        if self.settings["sound"] and self.audio_available and sound:
            sound.play()

    def load_settings(self):
        default_data = {
            "snake_color": [0, 255, 0],
            "grid": True,
            "sound": True
        }

        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "snake_color" not in data:
                        data["snake_color"] = default_data["snake_color"]
                    if "grid" not in data:
                        data["grid"] = default_data["grid"]
                    if "sound" not in data:
                        data["sound"] = default_data["sound"]
                    return data
            except Exception:
                pass

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)

        return default_data

    def save_settings(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def reset_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = self.direction
        self.score = 0
        self.level = 1
        self.food_eaten_for_level = 0
        self.speed = FPS
        self.active_effect = None
        self.effect_end = 0
        self.shield = False
        self.obstacles = set()
        self.food = None
        self.poison_food = None
        self.powerup = None
        self.powerup_spawn_time = 0
        self.last_powerup_spawn = pygame.time.get_ticks()
        self.final_saved = False
        self.spawn_foods()

    def valid_cells(self):
        cells = []
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            for y in range(80, WINDOW_HEIGHT, GRID_SIZE):
                cells.append((x, y))
        return cells

    def free_cells(self):
        used = set(self.snake) | self.obstacles

        if self.food:
            used.add(self.food["pos"])
        if self.poison_food:
            used.add(self.poison_food["pos"])
        if self.powerup:
            used.add(self.powerup["pos"])

        return [c for c in self.valid_cells() if c not in used]

    def random_free_position(self):
        cells = self.free_cells()
        return random.choice(cells) if cells else None

    def spawn_foods(self):
        pos1 = self.random_free_position() or (200, 200)
        pos2 = self.random_free_position() or (300, 200)

        self.food = {
            "pos": pos1,
            "value": random.choice([1, 2, 3]),
            "spawned_at": pygame.time.get_ticks(),
            "lifetime": 7000
        }

        self.poison_food = {
            "pos": pos2,
            "spawned_at": pygame.time.get_ticks()
        }

    def maybe_respawn_normal_food(self):
        now = pygame.time.get_ticks()
        if now - self.food["spawned_at"] > self.food["lifetime"]:
            pos = self.random_free_position()
            if pos:
                self.food = {
                    "pos": pos,
                    "value": random.choice([1, 2, 3]),
                    "spawned_at": now,
                    "lifetime": 7000
                }

    def maybe_spawn_powerup(self):
        now = pygame.time.get_ticks()
        if self.powerup is None and now - self.last_powerup_spawn > 9000:
            pos = self.random_free_position()
            if pos:
                kind = random.choice(list(POWER_UPS.keys()))
                self.powerup = {"kind": kind, "pos": pos}
                self.powerup_spawn_time = now
                self.last_powerup_spawn = now

    def update_powerup_timers(self):
        now = pygame.time.get_ticks()

        if self.powerup and now - self.powerup_spawn_time > 8000:
            self.powerup = None

        if self.active_effect in ("speed", "slow") and now > self.effect_end:
            self.active_effect = None
            self.speed = FPS + (self.level - 1) * 2

    def apply_powerup(self, kind):
        now = pygame.time.get_ticks()

        if kind == "speed":
            self.active_effect = "speed"
            self.effect_end = now + POWER_UPS["speed"]["duration"]
            self.speed = FPS + (self.level - 1) * 2 + 5

        elif kind == "slow":
            self.active_effect = "slow"
            self.effect_end = now + POWER_UPS["slow"]["duration"]
            self.speed = max(5, FPS + (self.level - 1) * 2 - 4)

        elif kind == "shield":
            self.active_effect = "shield"
            self.shield = True

    def place_obstacles_for_level(self):
        if self.level < 3:
            self.obstacles = set()
            return

        obstacle_count = min(6 + self.level, 20)
        self.obstacles = set()
        attempts = 0

        protected = set(self.snake)
        head_x, head_y = self.snake[0]
        for dx in (-GRID_SIZE, 0, GRID_SIZE):
            for dy in (-GRID_SIZE, 0, GRID_SIZE):
                protected.add((head_x + dx, head_y + dy))

        while len(self.obstacles) < obstacle_count and attempts < 1500:
            attempts += 1
            pos = (
                random.randrange(0, WINDOW_WIDTH, GRID_SIZE),
                random.randrange(80, WINDOW_HEIGHT, GRID_SIZE)
            )

            if pos in protected:
                continue
            self.obstacles.add(pos)

    def level_up_if_needed(self):
        if self.food_eaten_for_level >= 5:
            self.food_eaten_for_level = 0
            self.level += 1
            self.speed = FPS + (self.level - 1) * 2
            self.place_obstacles_for_level()

    def save_result_once(self):
        if self.final_saved or not self.username.strip() or not self.db_ready:
            return

        try:
            db.save_result(self.username.strip(), self.score, self.level)
        except Exception as e:
            print("Save result error:", e)

        self.final_saved = True

    def game_over(self):
        self.play_sound(self.death_sound)
        self.save_result_once()

        if self.db_ready and self.username.strip():
            try:
                self.personal_best = db.get_personal_best(self.username.strip())
            except Exception:
                pass

        self.state = "game_over"

    def turn_after_shield(self):
        head_x, head_y = self.snake[0]
        candidates = [(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)]
        random.shuffle(candidates)

        for dx, dy in candidates:
            nx, ny = head_x + dx, head_y + dy
            if (
                0 <= nx < WINDOW_WIDTH and
                80 <= ny < WINDOW_HEIGHT and
                (nx, ny) not in self.snake and
                (nx, ny) not in self.obstacles
            ):
                self.direction = (dx, dy)
                self.next_direction = (dx, dy)
                return

        self.game_over()

    def update(self):
        self.maybe_respawn_normal_food()
        self.maybe_spawn_powerup()
        self.update_powerup_timers()

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        hit_wall = not (0 <= new_head[0] < WINDOW_WIDTH and 80 <= new_head[1] < WINDOW_HEIGHT)
        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_wall or hit_self:
            if self.shield:
                self.shield = False
                self.active_effect = None
                self.turn_after_shield()
                return
            self.game_over()
            return

        if hit_obstacle:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food["pos"]:
            self.score += self.food["value"]
            self.food_eaten_for_level += 1
            self.play_sound(self.eat_sound)
            self.level_up_if_needed()

            pos = self.random_free_position()
            if pos:
                self.food = {
                    "pos": pos,
                    "value": random.choice([1, 2, 3]),
                    "spawned_at": pygame.time.get_ticks(),
                    "lifetime": 7000
                }

        elif new_head == self.poison_food["pos"]:
            self.play_sound(self.eat_sound)

            for _ in range(2):
                if len(self.snake) > 0:
                    self.snake.pop()

            if len(self.snake) <= 1:
                self.game_over()
                return

            pos = self.random_free_position()
            if pos:
                self.poison_food = {
                    "pos": pos,
                    "spawned_at": pygame.time.get_ticks()
                }

        elif self.powerup and new_head == self.powerup["pos"]:
            self.apply_powerup(self.powerup["kind"])
            self.powerup = None
            self.snake.pop()

        else:
            self.snake.pop()

    def draw_text_center(self, text, y, font=None, color=TEXT_COLOR):
        font = font or self.font
        surf = font.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=(WINDOW_WIDTH // 2, y)))

    def draw_grid(self):
        if not self.settings["grid"]:
            return
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (35, 35, 35), (x, 80), (x, WINDOW_HEIGHT))
        for y in range(80, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (35, 35, 35), (0, y), (WINDOW_WIDTH, y))

    def draw_game(self):
        if self.main_bg:
            self.screen.blit(self.main_bg, (0, 0))
        else:
            self.screen.fill(BG_COLOR)

        self.draw_grid()

        hud = f"User: {self.username or 'Guest'}   Score: {self.score}   Level: {self.level}   Best: {self.personal_best}"
        self.screen.blit(self.small_font.render(hud, True, TEXT_COLOR), (15, 20))

        effect_text = "Shield: ON" if self.shield else f"Effect: {self.active_effect or 'None'}"
        self.screen.blit(self.small_font.render(effect_text, True, TEXT_COLOR), (15, 48))

        snake_color = tuple(self.settings["snake_color"])
        for segment in self.snake:
            pygame.draw.rect(self.screen, snake_color, (*segment, GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(self.screen, FOOD_COLOR, (*self.food["pos"], GRID_SIZE, GRID_SIZE))
        food_value_txt = self.small_font.render(str(self.food["value"]), True, (0, 0, 0))
        self.screen.blit(food_value_txt, (self.food["pos"][0] + 5, self.food["pos"][1] + 1))

        pygame.draw.rect(self.screen, POISON_COLOR, (*self.poison_food["pos"], GRID_SIZE, GRID_SIZE))

        for block in self.obstacles:
            pygame.draw.rect(self.screen, OBSTACLE_COLOR, (*block, GRID_SIZE, GRID_SIZE))

        if self.powerup:
            color = POWER_UPS[self.powerup["kind"]]["color"]
            pygame.draw.rect(self.screen, color, (*self.powerup["pos"], GRID_SIZE, GRID_SIZE))

    def draw_menu(self):
        self.screen.fill((15, 15, 25))
        self.draw_text_center("Snake Game TSIS 3", 100, self.big_font)

        user_label = self.font.render("Username:", True, TEXT_COLOR)
        self.screen.blit(user_label, (220, 155))

        pygame.draw.rect(self.screen, (60, 60, 60), (320, 145, 260, 40), border_radius=8)
        pygame.draw.rect(self.screen, (180, 180, 180), (320, 145, 260, 40), 2, border_radius=8)

        user_text = self.font.render(self.username if self.username else "Type here...", True, TEXT_COLOR)
        self.screen.blit(user_text, (330, 152))

        if not self.db_ready:
            warn = self.small_font.render("Database is not connected. Leaderboard/save will not work.", True, (255, 120, 120))
            self.screen.blit(warn, warn.get_rect(center=(WINDOW_WIDTH // 2, 500)))

        for button in self.menu_buttons:
            button.draw(self.screen, self.font)

    def draw_leaderboard(self):
        self.screen.fill((20, 20, 30))
        self.draw_text_center("Top 10 Leaderboard", 60, self.big_font)

        headers = ["Rank", "Username", "Score", "Level", "Date"]
        x_positions = [70, 150, 350, 460, 560]

        for i, h in enumerate(headers):
            self.screen.blit(self.small_font.render(h, True, (255, 220, 120)), (x_positions[i], 110))

        rows = []
        if self.db_ready:
            try:
                rows = db.get_top_10()
            except Exception as e:
                print("Leaderboard error:", e)

        y = 150
        if rows:
            for idx, row in enumerate(rows, start=1):
                username, score, level, played_at = row
                values = [str(idx), str(username), str(score), str(level), played_at.strftime("%Y-%m-%d")]
                for i, val in enumerate(values):
                    self.screen.blit(self.small_font.render(val, True, TEXT_COLOR), (x_positions[i], y))
                y += 35
        else:
            self.draw_text_center("No leaderboard data yet.", 220, self.font)

        self.back_button.draw(self.screen, self.small_font)

    def draw_settings(self):
        self.screen.fill((25, 20, 20))
        self.draw_text_center("Settings", 70, self.big_font)

        grid_text = self.font.render(f"Grid Overlay: {'ON' if self.settings['grid'] else 'OFF'}  (press G)", True, TEXT_COLOR)
        sound_text = self.font.render(f"Sound: {'ON' if self.settings['sound'] else 'OFF'}  (press S)", True, TEXT_COLOR)
        color_text = self.font.render("Snake Color:", True, TEXT_COLOR)

        self.screen.blit(grid_text, (180, 180))
        self.screen.blit(sound_text, (180, 250))
        self.screen.blit(color_text, (180, 330))

        for rect_data, color in self.color_buttons:
            rect = pygame.Rect(rect_data)
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            if tuple(self.settings["snake_color"]) == color:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=6)

        self.save_back_button.draw(self.screen, self.font)

    def draw_game_over(self):
        if self.game_over_bg:
            self.screen.blit(self.game_over_bg, (0, 0))
        else:
            self.screen.fill((35, 15, 15))

        self.draw_text_center("Game Over", 120, self.big_font, (255, 110, 110))
        self.draw_text_center(f"Final Score: {self.score}", 220, self.font)
        self.draw_text_center(f"Level Reached: {self.level}", 260, self.font)
        self.draw_text_center(f"Personal Best: {self.personal_best}", 300, self.font)

        for button in self.game_over_buttons:
            button.draw(self.screen, self.font)

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif event.key == pygame.K_RETURN:
                if self.username.strip():
                    if self.db_ready:
                        try:
                            self.personal_best = db.get_personal_best(self.username.strip())
                        except Exception:
                            self.personal_best = 0
                    self.reset_game()
                    self.state = "playing"
            else:
                if len(self.username) < 16 and event.unicode.isprintable():
                    self.username += event.unicode

        for button in self.menu_buttons:
            if button.is_clicked(event):
                if button.text == "Play":
                    if self.username.strip():
                        if self.db_ready:
                            try:
                                self.personal_best = db.get_personal_best(self.username.strip())
                            except Exception:
                                self.personal_best = 0
                        self.reset_game()
                        self.state = "playing"
                elif button.text == "Leaderboard":
                    self.state = "leaderboard"
                elif button.text == "Settings":
                    self.state = "settings"
                elif button.text == "Quit":
                    pygame.quit()
                    raise SystemExit

    def handle_settings_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                self.settings["grid"] = not self.settings["grid"]
            elif event.key == pygame.K_s:
                self.settings["sound"] = not self.settings["sound"]

        if self.save_back_button.is_clicked(event):
            self.save_settings()
            self.state = "menu"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect_data, color in self.color_buttons:
                rect = pygame.Rect(rect_data)
                if rect.collidepoint(event.pos):
                    self.settings["snake_color"] = list(color)

    def handle_leaderboard_event(self, event):
        if self.back_button.is_clicked(event):
            self.state = "menu"

    def handle_game_over_event(self, event):
        for button in self.game_over_buttons:
            if button.is_clicked(event):
                if button.text == "Retry":
                    self.reset_game()
                    self.state = "playing"
                elif button.text == "Main Menu":
                    self.state = "menu"

    def handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, GRID_SIZE):
                self.next_direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and self.direction != (0, -GRID_SIZE):
                self.next_direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and self.direction != (GRID_SIZE, 0):
                self.next_direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-GRID_SIZE, 0):
                self.next_direction = (GRID_SIZE, 0)
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if self.state == "menu":
                    self.handle_menu_event(event)
                elif self.state == "settings":
                    self.handle_settings_event(event)
                elif self.state == "leaderboard":
                    self.handle_leaderboard_event(event)
                elif self.state == "game_over":
                    self.handle_game_over_event(event)
                elif self.state == "playing":
                    self.handle_playing_event(event)

            if self.state == "playing":
                self.update()
                self.draw_game()
                self.clock.tick(self.speed)
            elif self.state == "menu":
                self.draw_menu()
                self.clock.tick(30)
            elif self.state == "leaderboard":
                self.draw_leaderboard()
                self.clock.tick(30)
            elif self.state == "settings":
                self.draw_settings()
                self.clock.tick(30)
            elif self.state == "game_over":
                self.draw_game_over()
                self.clock.tick(30)

            pygame.display.flip()