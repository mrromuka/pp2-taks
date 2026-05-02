import pygame
import random


pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

FPS = 60
FramePerSec = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)


SPEED = 5


SCORE = 0
COINS = 0


font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 40)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

     
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE

        self.rect.move_ip(0, SPEED)

      
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)



class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

  
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 215, 0))

        self.rect = self.image.get_rect()

        self.weight = random.choice([1, 2, 5])

        self.reset()

    def reset(self):
   
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
        self.weight = random.choice([1, 2, 5])

    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()



P1 = Player()
E1 = Enemy()
C1 = Coin()


enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)


INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 3000)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

       
        if event.type == INC_SPEED:
            SPEED += 0.5

    DISPLAYSURF.fill(WHITE)


    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()


    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        game_over = font_big.render("GAME OVER", True, BLACK)
        DISPLAYSURF.blit(game_over, (70, 250))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

   
    hit_coin = pygame.sprite.spritecollideany(P1, coins)
    if hit_coin:
        COINS += hit_coin.weight
        hit_coin.reset()

    if COINS >= 10:
        SPEED = 7
    if COINS >= 20:
        SPEED = 9
    if COINS >= 30:
        SPEED = 12

   
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)

    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (10, 40))

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()