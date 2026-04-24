import pygame
import sys
import math
from datetime import datetime

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()


bg = pygame.image.load("clock.jpg")  
bg = pygame.transform.scale(bg, (500, 500))


right_hand = pygame.image.load("right-hand.png")  
left_hand = pygame.image.load("left-hand.png")    


center = (250, 250)

def draw_hand(image, angle):
   
    rotated = pygame.transform.rotate(image, -angle)

    rect = rotated.get_rect(center=center)

    
    screen.blit(rotated, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    now = datetime.now()
    minutes = now.minute
    seconds = now.second

   
    minute_angle = (minutes / 60) * 360
    second_angle = (seconds / 60) * 360

    screen.blit(bg, (0, 0))

    draw_hand(right_hand, minute_angle)  
    draw_hand(left_hand, second_angle)   

    pygame.display.update()
    clock.tick(60)