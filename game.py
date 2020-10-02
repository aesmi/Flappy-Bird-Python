import pygame, sys

#initialize an instance of pygame
pygame.init()
#sets canvas size for display surface (there can only be one display surface)
screen = pygame.display.set_mode((576,1024))
#sets ingame clock speed
clock = pygame.time.Clock()

#loads background image as a new surface
#convert changes the image to something thats easier to work with in pygame
bg_surface=pygame.image.load('assets/background-day.png').convert()
#scales image up to 2x
bg_surface=pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base/bg_surface')

#uses while loop to constantly call update method in order to refresh the screen
while True:
    #for every event that happens within the instance of pygame execute this block of code
    for event in pygame.event.get():
        #if event type is quit, run quit method
        #this also exits the while loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #1st argument is the image you want to pass in
    #2nd argument is a tuple of x and y coordinates of the left corner of the surface
    screen.blit(bg_surface, (0,0))

    pygame.display.update()
    #120 tickrate
    #this most likely sends a delay until 1000/tick_rate has passed
    clock.tick(120)