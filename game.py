import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mon premier jeu")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 28)
x = 400
y = 300
speed = 3
size = 50

mode = "menu"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               mode = "game"
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if mode == "menu":
                    mode = "game"   
    
    if mode == "game":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += speed
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y += speed
    
        if x < 0:
            x = 0
        if x > 800 - size:
            x = 800 - size
        if y < 0:                                   
            y = 0
        if y > 600 - size:
            y = 600 - size

    clock.tick(60)
    
    screen.fill((0, 0, 0))
    if mode == "menu":
       title = font.render("Mon premier jeu", True, (255, 255, 255))
       hint = small_font.render("ENTRÉE = jouer | ÉCHAP = quitter", True, (200, 200, 200))
       screen.blit(title, (200, 200))
       screen.blit(hint, (200, 260))
    elif mode == "game":
        pygame.draw.rect(screen, (255, 255, 255), (x, y, size, size))
    pygame.display.flip()

pygame.quit()
