import sys, pygame
pygame.init()

size = width, height = 500, 500
speed = [1, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ogre = pygame.image.load("Ogre.jpg")
w, h = ogre.get_size()
ogre = pygame.transform.smoothscale(ogre, (w//3,h//3))
ogreRect = ogre.get_rect()

tanith = pygame.image.load("tanith.jpg")
w, h = tanith.get_size()
tanith = pygame.transform.smoothscale(tanith, (w//3,h//3))
tanithRect = tanith.get_rect()
tanithRect.move_ip((250, 100))

rects = [ogreRect, tanithRect]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    tanithRect.move((1,1))
    for rect in rects:
        rect.move_ip(speed)
        if rect.left < 0 or rect.right > width:
            speed[0] = -speed[0]
        if rect.top < 0 or rect.bottom > height:
            speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ogre, ogreRect)
    screen.blit(tanith, tanithRect)
    pygame.display.flip()
    pygame.time.wait(1)
