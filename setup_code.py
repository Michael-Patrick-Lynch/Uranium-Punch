import pygame
from pygame import *
from globals import *
pygame.init()


ground_colour = (25,30,25)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

floor_level = 600
scroll_speed = 12
distance_between_building_centroids = 86
time_between_waves = 10000


# setting up window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Uranium_Punch')
SCREEN.fill(ground_colour)

# pallet swap function
def pallet_swap(surf, old_colour, new_colour):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_colour)
    surf.set_colorkey(old_colour)
    img_copy.blit(surf, (0,0))
    return img_copy


# syntactic sugar
ATTACKING = 'attacking'
ADVANCING = 'advancing'
IDLING = 'idling'
DYING = 'dying'

# time
fpsClock = pygame.time.Clock()
FPS = 60
one_second_has_passed = USEREVENT + 10 # this is an event that is triggered every second, and when it is triggered I will do all the things I want to do every second
pygame.time.set_timer(one_second_has_passed, 1000)
two_seconds_have_passed = USEREVENT + 11
pygame.time.set_timer(two_seconds_have_passed, 2000)

# images
background_sky_image = pygame.image.load('bg.png')
background_building_image = pygame.transform.scale(pygame.image.load('buildings.png'), (2800, floor_level))
background_building_rect = pygame.Rect(0,0,2800, floor_level)


player_base_image = pygame.transform.scale(pygame.image.load('player_base.png'), (366 * 3, 140 * 3))
player_base_rect = player_base_image.get_rect()
player_base_rect.bottomleft = (0, floor_level)
enemy_base_rect = pygame.Rect(2800-366, 700 - 50 - 140, 366, 140)

# code for loading the tilemap
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

grass_img = pygame.transform.scale(pygame.image.load('tile1.png'), (25, 25))
dirt_img =  pygame.transform.scale(pygame.image.load('tile2.png'), (25, 25))
bedrock_img = pygame.transform.scale(pygame.image.load('tile3.png'), (25, 25))

sky_img = pygame.transform.scale(pygame.image.load('sky.png'), (2800, 700))


light_infantry_icon_image = pygame.image.load('light_infantry_icon.png')
light_infantry_icon_rect = pygame.Rect(50, 25, 50, 50)
light_infantry_icon_rect.center = (900, 650)

# knight_icon_image = pygame.image.load('knight_icon.png')
# knight_icon_rect = pygame.Rect(50, 25, 50, 50)
# knight_icon_rect.center = (970, 650)

infantry_icon = pygame.image.load('space_marine_icon.png')
infantry_icon_rect = pygame.Rect(50, 25, 50, 50)
infantry_icon_rect.center = (1040, 650)

wizard_icon_image = pygame.image.load('wizard_icon.png')
wizard_icon_rect = pygame.Rect(50, 25, 50, 50)
wizard_icon_rect.center = (1110, 650)

tank_icon_image = pygame.image.load('tank_icon.png')
tank_icon_rect = pygame.Rect(50, 25, 50, 50)
tank_icon_rect.center = (1180, 650)

troop_control_icon_image = pygame.image.load('arrows.png')
troop_control_icon_rect = pygame.Rect(500, 630, 200, 200)
troop_control_icon_rect.center = (650, 720)

drill_icon_image = pygame.image.load('drill_icon.png')
drill_icon_rect = pygame.Rect(200, 630, 75, 75)
drill_icon_rect.center = (100, 660)

reactor_icon_image = pygame.image.load('reactor_icon.png')
reactor_icon_rect = pygame.Rect(200, 200, 75, 75)
reactor_icon_rect.center = (175, 660)

lab_icon_image = pygame.image.load('lab_icon.png')
lab_icon_rect = pygame.Rect(200, 200, 75, 75)
lab_icon_rect.center = (250, 660)

GAME_SURFACE = pygame.transform.scale(sky_img, (2800, 700))
GAME_RECT = GAME_SURFACE.get_rect()



# USER_INTERFACE_SURF = pygame.transform.scale(background_sky_image, (2800, 100)) # could have used any image
USER_INTERFACE_SURF = pygame.surface.Surface((2800, 100))
USER_INTERFACE_SURF.fill(WHITE)

# the code to blit the tiles
tile_rects = []
y = 0
for layer in game_map:
    x = 0
    for tile in layer:
        if tile == '1':
            USER_INTERFACE_SURF.blit(dirt_img,(x*25,y*25))
        if tile == '2':
            USER_INTERFACE_SURF.blit(grass_img,(x*25,y*25))
        if tile == '3':
            USER_INTERFACE_SURF.blit(bedrock_img,(x*25,y*25))
        if tile != '0':
            tile_rects.append(pygame.Rect(x*25,y*25,25,25))
        x += 1
    y += 1

user_interface_rect = pygame.Rect(0, floor_level, 2800, 100)
USER_INTERFACE_SURF.blit(troop_control_icon_image, troop_control_icon_rect)
GAME_SURFACE.blit(USER_INTERFACE_SURF, user_interface_rect)
# SCREEN.blit(USER_INTERFACE_SURF, user_interface_rect)
print(f"{user_interface_rect}")

USER_INTERFACE_SURF = pygame.surface.Surface((2800, 100))


# music
pygame.mixer.music.load('industrial.mp3')
pygame.mixer.music.play(-1, 0)

# to reset the game or start the first game
def setup_game():
    print("setup_game() executed")
    global listOfBuildings,listOfTroops, listOfTroop_sorted_according_to_x_co_ord, listOfEnemies, listOfEnemies_sorted_according_to_x_co_ord, listOfBullets, listOfTanks, listOfExplosions
    global GAME_RECT, background_building_rect

    GAME_RECT.left, background_building_rect.left = 0, 0
    listOfBuildings.clear()
    print(id(listOfTroops))
    listOfTroops.clear()
    print(id(listOfTroops))
    print("******************************************************************")
    print("******************************************************************")
    print("******************************************************************")
    print("******************************************************************")
    print("******************************************************************")
    listOfTroop_sorted_according_to_x_co_ord.clear()

    listOfEnemies.clear()
    listOfEnemies_sorted_according_to_x_co_ord.clear()

    listOfBullets.clear()

    listOfTanks.clear() # since tanks fire only every 2 seconds
    listOfExplosions.clear()



# health
heartimg = pygame.transform.scale(pygame.image.load('heart.png'), (50, 50))
heart_rect = pygame.Rect(250, 100, 50, 50)
heart_rect.center = (250, 100)
player_health = 1000
player_health_font = pygame.font.Font('Pixeltype.ttf', 60)




