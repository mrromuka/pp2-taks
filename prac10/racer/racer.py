import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

player_img = pygame.image.load("player.png")
coin_img = pygame.image.load("coin.png")
enemy_img = pygame.image.load("enemy.png")
bg_img = pygame.image.load("AnimatedStreet.png")

player_img = pygame.transform.scale(player_img, (50, 100))
coin_img = pygame.transform.scale(coin_img, (40, 40))
enemy_img = pygame.transform.scale(enemy_img, (50, 100))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

player_x = 170
player_y = 480
speed = 5

coin_x = random.randint(50, 350)
coin_y = -100
coin_speed = 4

enemy_x = random.randint(50, 350)
enemy_y = -300
enemy_speed = 6

bg_y1 = 0
bg_y2 = -HEIGHT

score = 0

font = pygame.font.Font(None, 36)

game_over = False

while True:
    screen.blit(bg_img, (0, bg_y1))
    screen.blit(bg_img, (0, bg_y2))

    bg_y1 += 3
    bg_y2 += 3

    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += speed

        coin_y += coin_speed
        enemy_y += enemy_speed

        if coin_y > HEIGHT:
            coin_y = -100
            coin_x = random.randint(50, 350)

        if enemy_y > HEIGHT:
            enemy_y = -300
            enemy_x = random.randint(50, 350)

        player_rect = pygame.Rect(player_x, player_y, 50, 100)
        coin_rect = pygame.Rect(coin_x, coin_y, 40, 40)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 100)

        if player_rect.colliderect(coin_rect):
            score += 1
            coin_y = -100
            coin_x = random.randint(50, 350)

        if player_rect.colliderect(enemy_rect):
            game_over = True

    screen.blit(coin_img, (coin_x, coin_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))
    screen.blit(player_img, (player_x, player_y))

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if game_over:
        over = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over, (120, 250))

    pygame.display.flip()
    clock.tick(60)