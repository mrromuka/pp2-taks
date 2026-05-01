import pygame
import random
import os
from Persistence import add_score


WIDTH = 480
HEIGHT = 700
ROAD_LEFT = 90
ROAD_RIGHT = 390
LANE_COUNT = 3
LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // LANE_COUNT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 220, 0)
BLUE = (0, 120, 255)


def lane_x(lane_index):
    return ROAD_LEFT + lane_index * LANE_WIDTH + LANE_WIDTH // 2


class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.image = self.load_car_image(settings["car_color"])
        self.rect = self.image.get_rect(center=(lane_x(1), HEIGHT - 100))
        self.lane = 1
        self.has_shield = False
        self.active_powerup = None
        self.powerup_timer = 0
        self.repair_available = False

    def load_car_image(self, color):
        mapping = {
            "red": "Player_red.png",
            "blue": "Player_blue.png",
            "yellow": "player_yellow.png",
            "white": "player_white.png"
        }

        path = os.path.join("detals", mapping[color])
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (55, 95))

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.rect.centerx = lane_x(self.lane)

    def move_right(self):
        if self.lane < LANE_COUNT - 1:
            self.lane += 1
            self.rect.centerx = lane_x(self.lane)

    def activate_powerup(self, powerup_type):
        self.active_powerup = powerup_type

        if powerup_type == "nitro":
            self.powerup_timer = pygame.time.get_ticks() + 4000
            self.has_shield = False
            self.repair_available = False

        elif powerup_type == "shield":
            self.has_shield = True
            self.powerup_timer = 0
            self.repair_available = False

        elif powerup_type == "repair":
            self.repair_available = True
            self.powerup_timer = 0
            self.has_shield = False

    def update_powerup(self):
        if self.active_powerup == "nitro" and pygame.time.get_ticks() > self.powerup_timer:
            self.active_powerup = None

    def use_shield(self):
        if self.has_shield:
            self.has_shield = False
            self.active_powerup = None
            return True
        return False

    def use_repair(self):
        if self.repair_available:
            self.repair_available = False
            self.active_powerup = None
            return True
        return False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        image = pygame.image.load(os.path.join("detals", "enemy.png")).convert_alpha()
        self.image = pygame.transform.scale(image, (55, 95))
        self.rect = self.image.get_rect()
        self.rect.centerx = lane_x(random.randint(0, 2))
        self.rect.y = -120
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        image = pygame.image.load(os.path.join("detals", "coin.png")).convert_alpha()
        self.image = pygame.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.centerx = lane_x(random.randint(0, 2))
        self.rect.y = -50
        self.speed = speed
        self.value = random.choice([1, 2, 5])

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, kind="oil"):
        super().__init__()
        filename = "oil.png"
        image = pygame.image.load(os.path.join("detals", filename)).convert_alpha()
        self.image = pygame.transform.scale(image, (55, 55))
        self.rect = self.image.get_rect()
        self.rect.centerx = lane_x(random.randint(0, 2))
        self.rect.y = -80
        self.speed = speed
        self.kind = kind

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind = random.choice(["nitro", "shield", "repair"])
        filename = f"{self.kind}.png"
        image = pygame.image.load(os.path.join("detals", filename)).convert_alpha()
        self.image = pygame.transform.scale(image, (45, 45))
        self.rect = self.image.get_rect()
        self.rect.centerx = lane_x(random.randint(0, 2))
        self.rect.y = -70
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT or pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()


class MovingBarrier(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((80, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(lane_x(1), -30))
        self.speed = speed
        self.direction = random.choice([-1, 1])
        self.x_speed = 3

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.direction * self.x_speed

        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
            self.direction *= -1
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT
            self.direction *= -1

        if self.rect.top > HEIGHT:
            self.kill()


def safe_spawn_lane(player_lane):
    lanes = [0, 1, 2]
    if player_lane in lanes:
        lanes.remove(player_lane)
    return random.choice(lanes)


def get_difficulty_values(difficulty):
    if difficulty == "easy":
        return {
            "base_speed": 5,
            "enemy_spawn_delay": 1400,
            "obstacle_spawn_delay": 1800
        }
    elif difficulty == "hard":
        return {
            "base_speed": 8,
            "enemy_spawn_delay": 900,
            "obstacle_spawn_delay": 1200
        }
    else:
        return {
            "base_speed": 6,
            "enemy_spawn_delay": 1100,
            "obstacle_spawn_delay": 1500
        }


def run_game(screen, username, settings):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 18)

    difficulty_values = get_difficulty_values(settings["difficulty"])
    base_speed = difficulty_values["base_speed"]

    road_img = pygame.image.load(os.path.join("detals", "road.png")).convert()
    road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))
    road_y1 = 0
    road_y2 = -HEIGHT

    if settings["sound"]:
        try:
            pygame.mixer.music.load(os.path.join("detals", "background.wav"))
            pygame.mixer.music.play(-1)
        except:
            pass

    crash_sound = None
    if settings["sound"]:
        try:
            crash_sound = pygame.mixer.Sound(os.path.join("detals", "crash.wav"))
        except:
            crash_sound = None

    player = Player(settings)
    player_group = pygame.sprite.GroupSingle(player)
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    events = pygame.sprite.Group()

    coins_collected = 0
    distance = 0
    score = 0
    finished = False
    finish_distance = 5000

    last_enemy_spawn = 0
    last_coin_spawn = 0
    last_obstacle_spawn = 0
    last_powerup_spawn = 0
    last_event_spawn = 0

    while not finished:
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        speed_bonus = 3 if player.active_powerup == "nitro" else 0
        current_speed = base_speed + speed_bonus + (coins_collected // 10)

        distance += current_speed * 0.1
        if distance >= finish_distance:
            finished = True

        road_y1 += current_speed
        road_y2 += current_speed
        if road_y1 >= HEIGHT:
            road_y1 = -HEIGHT
        if road_y2 >= HEIGHT:
            road_y2 = -HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return {
                    "action": "quit"
                }

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

        if current_time - last_enemy_spawn > max(400, difficulty_values["enemy_spawn_delay"] - int(distance // 20)):
            enemy = Enemy(current_speed)
            enemy.rect.centerx = lane_x(safe_spawn_lane(player.lane))
            enemies.add(enemy)
            last_enemy_spawn = current_time

        if current_time - last_coin_spawn > 1000:
            coins.add(Coin(current_speed))
            last_coin_spawn = current_time

        if current_time - last_obstacle_spawn > max(500, difficulty_values["obstacle_spawn_delay"] - int(distance // 25)):
            obstacle = Obstacle(current_speed)
            obstacle.rect.centerx = lane_x(safe_spawn_lane(player.lane))
            obstacles.add(obstacle)
            last_obstacle_spawn = current_time

        if current_time - last_powerup_spawn > 6000:
            pu = PowerUp(current_speed)
            pu.rect.centerx = lane_x(random.randint(0, 2))
            powerups.add(pu)
            last_powerup_spawn = current_time

        if current_time - last_event_spawn > 5000:
            events.add(MovingBarrier(current_speed))
            last_event_spawn = current_time

        player.update_powerup()
        enemies.update()
        coins.update()
        obstacles.update()
        powerups.update()
        events.update()

        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            coins_collected += coin.value

        collected_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for pu in collected_powerups:
            player.activate_powerup(pu.kind)

        if pygame.sprite.spritecollide(player, obstacles, True):
            if player.use_shield():
                pass
            elif player.use_repair():
                pass
            else:
                if crash_sound:
                    crash_sound.play()
                finished = True

        if pygame.sprite.spritecollide(player, enemies, True):
            if player.use_shield():
                pass
            elif player.use_repair():
                pass
            else:
                if crash_sound:
                    crash_sound.play()
                finished = True

        if pygame.sprite.spritecollide(player, events, True):
            if player.use_shield():
                pass
            elif player.use_repair():
                pass
            else:
                if crash_sound:
                    crash_sound.play()
                finished = True

        score = int(coins_collected * 10 + distance)
        if player.active_powerup == "nitro":
            score += 20

        screen.blit(road_img, (0, road_y1))
        screen.blit(road_img, (0, road_y2))

        enemies.draw(screen)
        coins.draw(screen)
        obstacles.draw(screen)
        powerups.draw(screen)
        events.draw(screen)
        player_group.draw(screen)

        pygame.draw.rect(screen, BLACK, (10, 10, 220, 120))
        pygame.draw.rect(screen, WHITE, (10, 10, 220, 120), 2)

        screen.blit(font.render(f"Coins: {coins_collected}", True, WHITE), (20, 20))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 50))
        screen.blit(font.render(f"Distance: {int(distance)}", True, WHITE), (20, 80))

        remaining = max(0, int(finish_distance - distance))
        screen.blit(small_font.render(f"Finish left: {remaining}", True, YELLOW), (20, 110))

        active_text = "None"
        if player.active_powerup:
            active_text = player.active_powerup.capitalize()

        screen.blit(small_font.render(f"Power-up: {active_text}", True, WHITE), (260, 20))

        if player.active_powerup == "nitro":
            time_left = max(0, (player.powerup_timer - pygame.time.get_ticks()) // 1000)
            screen.blit(small_font.render(f"Time: {time_left}s", True, GREEN), (260, 45))
        elif player.active_powerup == "shield":
            screen.blit(small_font.render("Blocks 1 hit", True, BLUE), (260, 45))
        elif player.active_powerup == "repair":
            screen.blit(small_font.render("1 extra save", True, GREEN), (260, 45))

        pygame.display.flip()

    pygame.mixer.music.stop()
    add_score(username, score, int(distance), coins_collected)

    return {
        "action": "game_over",
        "score": score,
        "distance": int(distance),
        "coins": coins_collected
    }