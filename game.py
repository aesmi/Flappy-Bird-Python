#imports
import pygame, sys, random 

#function used to draw floor for abstraction/simplfication
def draw_floor():
    #we use two floor surfaces to give the illusion of contuinity
    screen.blit(floor_surface, (floor_x_pos,900))
    screen.blit(floor_surface, (floor_x_pos + 576,900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos-200))
    return bottom_pipe, top_pipe
 
 #argument passed is a list of all pipes   
def move_pipes(pipes):
    #iterate through every pipe
    for pipe in pipes:
        #move pipe and its associated rect/hitbox to the left during each tick
        pipe.centerx -=5
    #return the modified list of pipes
    return pipes
    
def draw_pipes(pipes):
    #iterable lists of pipes generated by SPAWNPIPE event
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            #applies transformation to surface
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        #collide detection method for rectangles, arguments are coordinates (x,y)
        if bird_rect.colliderect(pipe):
            #audio
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom>=900:
        return False
    return True

def rotate_bird(bird):
    #(surface, degrees of rotation from cw, scale)
    new_bird=pygame.transform.rotozoom(bird, -bird_movement*4, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(str(int(score)), True, (255,255,255))
        high_score_rect = score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,score_rect)
    #else:
        #raise Exception("game_state argument is not valid")
def update_score(score, high_score):
    if score>high_score:
        high_score=score
    return high_score

#mixer pre_init
pygame.mixer.pre_init(frequency= 44100, size = 16, channels=1, buffer=512)
#initialize an instance of pygame
pygame.init()
#set canvas size for display surface (there can only be one display surface)
screen = pygame.display.set_mode((576,1024))
#set ingame clock
clock = pygame.time.Clock()
#set font
game_font = pygame.font.Font('04B_19.ttf',48)

#Game Variables
gravity = 0.25
bird_movement = 0
#space between pipes, planning to adding way to change this via gui, preferably via sliders
#space_between = 300
game_active=True
score = 0
high_score = 0

#loads background image as a new surface
#convert changes the image to something thats easier to work with in pygame
bg_surface=pygame.image.load('assets/background-day.png').convert()
#scales image up to 2x
bg_surface=pygame.transform.scale2x(bg_surface)
#Floor assets
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface=pygame.transform.scale2x(floor_surface)
floor_x_pos=0
#Bird assets
#bluebird
bluebird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bluebird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bluebird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
#redbird
redbird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
redbird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())
redbird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
#yellowbird
yellowbird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
yellowbird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
yellowbird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
#bird_frames/RGB birb
bird_frames = [bluebird_midflap,bluebird_upflap,bluebird_downflap, redbird_midflap,redbird_upflap,redbird_downflap,yellowbird_midflap,yellowbird_upflap,yellowbird_downflap]
#bird with frames
bird_index = 0
bird_surface = bird_frames[bird_index]
#this creates a rectangle and a point described in a tuple as x and y coordinates
bird_rect = bird_surface.get_rect(center = (100,512))

#flap event
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

#Pipe assets
pipe_surface = pygame.transform.scale2x( pygame.image.load('assets/pipe-green.png').convert())
#list to hold each instance of pipe and their respective properties
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
#python "callback" that triggers every 1200 ms or 1.2 seconds
pygame.time.set_timer(SPAWNPIPE, 800)
#random pipe height list
pipe_height=[400,500,600,700,800]

#Game Over screen
game_over_surface =  pygame.transform.scale2x( pygame.image.load('assets/message.png'))
game_over_rect = game_over_surface.get_rect(center = (288,512))

#Hitsound assets
flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')
score_sound=pygame.mixer.Sound('sound/sfx_point.wav')
death_sound=pygame.mixer.Sound('sound/sfx_die.wav')
#score countdown to round to whole
score_sound_countdown = 100

#uses while loop to constantly call update method in order to refresh the screen
#this is basically a hook
while True:
    #for every event that happens within the instance of pygame execute this block of code
    for event in pygame.event.get():
        #if event type is quit, run quit method
        #this also exits the while loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #run this block of code on every keydown/keypress event
        if event.type == pygame.KEYDOWN:
            #K_SPACE is spacebar
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                #reset all game parameters
                game_active=True
                pipe_list.clear()
                bird_rect.center(100,512)
                bird_movement = 0
                score = 0
        #if the spawnpipe event is passed, the create_pipe function is called
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        #if birbflap event is passed, the birb animation function is called
        if event.type == BIRDFLAP:
            if bird_index < 8:
                bird_index +=1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    #1st argument is the image you want to pass in
    #2nd argument is a tuple of x and y coordinates of the left corner of the surface
    screen.blit(bg_surface, (0,0))
    #Bird
    if game_active:
        #adds gravity
        bird_movement += gravity
        rotated_bird=rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        #this renders the bird image as well as the hitbox associated with it
        #first argument is the image, second argument is the hitbox
        screen.blit(rotated_bird, bird_rect)
        #Check collisions
        game_active = check_collision(pipe_list)
        #Pipes
        pipe_list = move_pipes(pipe_list)
        #call draw pipe function for each pipe in the list
        draw_pipes(pipe_list)
        score +=0.01
        score_display('main_game')
        score_sound_countdown -=1
        if score_sound_countdown <=0:
            score_sound.play()
            score_sound_countdown=100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    
    #Floor
    floor_x_pos -=1
    #call function to draw floor
    draw_floor()
    #reset floor position
    if floor_x_pos <= -576:
        floor_x_pos=0
    #calls display render update
    pygame.display.update()
    #120 tickrate
    #this most likely sends a delay until 1000/tick_rate has passed
    clock.tick(120)