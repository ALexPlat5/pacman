import pygame

window = pygame.display.set_mode((400, 400))

qub = [(0, 0), (150, 150), (250, 250)]

keys = pygame.key.get_pressed()
print(pygame.K_UP)
run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

    for i in qub:
        pygame.draw.rect(window, (255, 255, 8), (*i, 40, 40))
    pygame.display.update()

pygame.quit()
