import pygame, sys

pygame.init()

screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music Player")

tracks = ["123.mp3", "123.mp3", "123.mp3"]
current = 0
playing = False

pygame.mixer.music.load(tracks[current])

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if i.type == pygame.KEYDOWN:

            if i.key == pygame.K_p:
                pygame.mixer.music.load(tracks[current])
                pygame.mixer.music.play()
                playing = True

            if i.key == pygame.K_s:
                pygame.mixer.music.stop()
                playing = False

            if i.key == pygame.K_n:
                current += 1
                if current >= len(tracks):
                    current = 0
                pygame.mixer.music.load(tracks[current])
                pygame.mixer.music.play()
                playing = True

            if i.key == pygame.K_b:
                current -= 1
                if current < 0:
                    current = len(tracks) - 1
                pygame.mixer.music.load(tracks[current])
                pygame.mixer.music.play()
                playing = True

            if i.key == pygame.K_q:
                pygame.quit()
                sys.exit()

   
    screen.fill((20, 20, 20))

   
    textP = font.render("P - Play", True, (255,255,255))
    textS = font.render("S - Stop", True, (255,255,255))
    textB = font.render("B - Back", True, (255,255,255))
    textN = font.render("N - Next", True, (255,255,255))

    screen.blit(textP, (20, 20))
    screen.blit(textS, (160, 20))
    screen.blit(textB, (300, 20))
    screen.blit(textN, (440, 20))

   
    track_text = font.render(f"Track: {tracks[current]}", True, (200,200,200))
    screen.blit(track_text, (20, 100))

   
    status = "Playing" if playing else "Stopped"
    status_text = font.render(f"Status: {status}", True, (0,255,0) if playing else (255,0,0))
    screen.blit(status_text, (20, 150))


    pos = pygame.mixer.music.get_pos() // 1000
    time_text = font.render(f"Time: {pos} sec", True, (180,180,180))
    screen.blit(time_text, (20, 200))

    pygame.display.update()
    clock.tick(60)