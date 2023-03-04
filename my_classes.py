import pygame
from pygame import *
from setup_code import *
from spritesheet import *
from globals import *
pygame.init()

# extractSprites is a function I got from stackoverflow
def extractSprites(rows, columns, sprite_width, sprite_height, sprites, name_of_sprite_sheet_file, xsize, ysize):
    sprite_sheet = pygame.image.load(name_of_sprite_sheet_file).convert_alpha()
    sprite_sheet.set_colorkey((0,0,0))
    for row in range(rows):
        for column in range(columns):
            x = column * sprite_width
            y = row * sprite_height
            width = sprite_width
            height = sprite_height

            # Use subsurface to extract the sprite
            sprite = sprite_sheet.subsurface((x, y, width, height))
            scaled_sprite = pygame.transform.scale(sprite, (xsize, ysize))

            # Add the sprite to the list
            sprites.append(scaled_sprite)

class Troop(pygame.sprite.Sprite):
    global listOfTroops, listOfBullets
    
    speed = 8
    attack_damage = 20
    attack_delay = 2.5
    attack_range = 30
    blocked = False
    
    activity = ADVANCING # activity attribute will determine what animation plays and what the troop is doing
    # 'advancing' means the troop moves forward. True if blocked is False and enemy_in_range is False
    # 'idling' means the troop stands still. True if blocked is True and enemy_in_range is False
    # 'attacking' means the troop is attacking the enemy in front. True enemy_in_range is True
    # 'dying' means that troop object is going to play the die animation and then be deleted. True if health <= 0. Checked last to overwrite the other checks
    


    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)
        self.enemy_in_range = False
        self.health = 100

    def advanceForward(self):
        self.rect.x += self.speed

    def checkCurrentActivity(self):
        if self.enemy_in_range == True and self.blocked == True:
            self.activity = ATTACKING
        elif self.blocked == True:
            self.activity = IDLING
        else:
            self.activity = ADVANCING
        if self.health <= 0:
            self.activity = DYING

    def __lt__(self, other):
        return self.rect.x < other.rect.x
    
    def check_If_Dying(self):
        if self.health <= 0:
            listOfTroops.remove(self)
            del(self)


    
# attack due is set to False since this is a shooting troop
class Infantry(Troop):
    global listOfBullets
    rows = 1
    columns = 11
    sprites = []
    sprite_width = 48
    sprite_height = 48
    width_of_infantry = 100
    height_of_infantry = 100
    attack_range = 300
    attack_damage = 20
    metal_cost = 400
    energy_cost = 100
    
    
    updateImgEvent = USEREVENT + 2
    purchase_cooldown_over = USEREVENT + 3
    purchase_cooldown_active = False
    

    extractSprites(1, 11, sprite_width, sprite_height, sprites, 'space-marine-run.png', width_of_infantry, height_of_infantry) # 0 to 10 are running
    extractSprites(1, 2, 64, sprite_height, sprites, 'space-marine-shoot.png', width_of_infantry, height_of_infantry) # 11 to 12 are shooting
    extractSprites(1, 4, 48, 48, sprites, 'space-marine-idle.png', width_of_infantry, height_of_infantry) # 13 to 16 are idle
    current_sprite = 0
    image = sprites[0]
    
    

    def __init__(self, resource_system):
        
        self.rect = pygame.Rect(GAME_RECT.left + 20, floor_level, self.width_of_infantry, self.height_of_infantry)
        self.rect.bottom = floor_level + 5
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.enemy_in_range = False
        self.health = 100
        self.resource_system = resource_system
        self.resource_system.metal_level -= Infantry.metal_cost
        self.resource_system.energy_level -= Infantry.energy_cost
        self.attack_due = False
        
        pygame.time.set_timer(self.updateImgEvent, 75)
    
    def updateImage(self):
        # if self.shooting == True:
        if self.activity == ATTACKING:
            if self.current_sprite != (11 or 12):
                self.current_sprite = 11
            elif self.current_sprite == 11:
                self.current_sprite = 12
                listOfBullets.append(Bullet(self))
            elif self.current_sprite == 12:
                self.current_sprite =  11

        elif self.activity == ADVANCING:
            if self.current_sprite >= 10:
                    self.current_sprite = 1
            else:
                self.current_sprite += 1

        elif self.activity == IDLING:
            if self.current_sprite < 13 or self.current_sprite >= 16:
                self.current_sprite = 13
            else:
                self.current_sprite += 1
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)



class LightInfantry(Troop):
    rows = 1
    columns = 6
    sprites = []
    sprite_width = 32
    sprite_height = 32
    width_of_infantry = 100
    height_of_infantry = 100
    attack_range = 300
    attack_damage = 10
    metal_cost = 100
    
    
    updateImgEvent = USEREVENT + 2
    purchase_cooldown_over = USEREVENT + 3
    purchase_cooldown_active = False

    extractSprites(1, 6, sprite_width, sprite_height, sprites, 'light_infantry_walk.png', width_of_infantry, height_of_infantry) # 0 to 5 are walking
    extractSprites(1, 3, sprite_width, sprite_height, sprites, 'light_infantry_shot.png', width_of_infantry, height_of_infantry) # 6 to 8 are shooting
    extractSprites(1, 1, sprite_width, sprite_height, sprites, 'light_infantry_crouch.png', width_of_infantry, height_of_infantry) # 9 is idling

    current_sprite = 0
    image = sprites[0]

    def __init__(self, resource_system):
        
        self.rect = pygame.Rect(GAME_RECT.left + 50, floor_level, self.width_of_infantry, self.height_of_infantry)
        self.rect.bottom = floor_level + 5
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.health = 100
        self.enemy_in_range = False
        self.activity = ADVANCING
        self.resource_system = resource_system
        self.resource_system.metal_level -= LightInfantry.metal_cost
        self.attack_due = False
        pygame.time.set_timer(self.updateImgEvent, 75)
    
    def updateImage(self):
        if self.activity == ATTACKING:
            if self.current_sprite < 6 or self.current_sprite >= 8:
                self.current_sprite = 6
                listOfBullets.append(Bullet(self))
            else:
                self.current_sprite += 1


        elif self.activity == ADVANCING:
            if self.current_sprite >= 5:
                    self.current_sprite = 1
            else:
                self.current_sprite += 1

        elif self.activity == IDLING:
            self.current_sprite = 9
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)



class Wizard(Troop):

    sprites = []
    sprite_width = 231
    sprite_height = 190
    width_of_infantry = 100
    height_of_infantry = 100
    attack_range = 300
    attack_damage = 2
    metal_cost = 400
    energy_cost = 100
    
    
    updateImgEvent = USEREVENT + 2
    purchase_cooldown_over = USEREVENT + 3
    purchase_cooldown_active = False
    
    running_sprite_sheet = SpriteSheet('wizard_run.png')
    attacking_sprite_sheet = SpriteSheet('wizard_attack.png')
    idling_sprite_sheet = SpriteSheet('wizard_idle.png')



    list_of_running_sprites = running_sprite_sheet.load_grid_images(1, 8, 73, 160, 30, 0)
    list_of_attacking_sprites = attacking_sprite_sheet.load_grid_images(1, 8, 170, 80, 30, 0)
    list_of_idling_sprites = idling_sprite_sheet.load_grid_images(1, 6, 73, 160, 30, 0)
    
    
    sprites.extend(list_of_running_sprites)
    sprites.extend(list_of_attacking_sprites)
    sprites.extend(list_of_idling_sprites)

    # extractSprites(1, 8, sprite_width, sprite_height, sprites, 'wizard_run.png', width_of_infantry, height_of_infantry) # 0 to 7 are running
    # extractSprites(1, 8, sprite_width, sprite_height, sprites, 'wizard_attack.png', width_of_infantry, height_of_infantry) # 8 to 15 are attacking
    # extractSprites(1, 6, sprite_width, sprite_height, sprites, 'wizard_idle.png', width_of_infantry, height_of_infantry) # 16 to 21 are idle
    current_sprite = 0
    image = sprites[0]
    
    

    def __init__(self, resource_system):
        
        self.rect = pygame.Rect(GAME_RECT.left + 20, floor_level, self.width_of_infantry, self.height_of_infantry)
        self.rect.bottom = floor_level - 10
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.enemy_in_range = False
        self.health = 100
        self.resource_system = resource_system
        self.resource_system.metal_level -= Wizard.metal_cost
        self.resource_system.energy_level -= Wizard.energy_cost
        self.attack_due = self.enemy_in_range
        
        pygame.time.set_timer(self.updateImgEvent, 75)
    
    def updateImage(self):
        # if self.shooting == True:
        if self.activity == ATTACKING:
            if self.current_sprite < 8 or self.current_sprite >= 15:
                self.current_sprite = 8
            else:
                self.current_sprite += 1
                listOfBullets.append(Bullet(self))


        elif self.activity == ADVANCING:
            if self.current_sprite >= 7:
                    self.current_sprite = 1
            else:
                self.current_sprite += 1

        elif self.activity == IDLING:
            if self.current_sprite < 16 or self.current_sprite >= 21:
                self.current_sprite = 16
            else:
                self.current_sprite += 1
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)

class PlayerTotem(Troop):
    speed = 0
    sprites = []
    updateImgEvent = USEREVENT + 2

    extractSprites(1, 4, 106, 77, sprites, 'spaceship-unit.png', 106*2, 77*2)

    current_sprite = 0
    

    def __init__(self):
        self.rect = pygame.Rect(GAME_RECT.left,475,106,77)
        self.enemy_in_range = False
        self.health = 50
        self.image = self.sprites[self.current_sprite]

    def updateImage(self):
        if self.current_sprite == 3:
            self.current_sprite = 1   
        else: 
            self.current_sprite = 1
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)


class Enemy(pygame.sprite.Sprite):
    global listOfEnemies
        
    speed = 1
    attack_damage = 20
    attack_delay = 2.5
    
  
    blocked = False
    enemy_in_range = False


    def __init__(self, that_games_resource_system):
        self.rect = pygame.Rect(0,0,0,0)
        self.mask = pygame.mask.from_surface(self.image)
        self.activity = 'advancing'
        self.health = 100
        self.resource_system = that_games_resource_system

    def advanceForward(self):
        self.rect.x -= self.speed

    def __lt__(self, other):
        return self.rect.x > other.rect.x
    

    def checkCurrentActivity(self):
            if self.enemy_in_range == True and self.blocked == True:
                self.activity = ATTACKING
            elif self.blocked == True:
                self.activity = IDLING
            else:
                self.activity = ADVANCING
            if self.health <= 0:
                self.activity = DYING

        
    def check_If_Dying(self):
        if self.health <= 0:
            self.resource_system.uranium_level += 40
            listOfEnemies.remove(self)
            del(self)
            #listOfEnemies_sorted_according_to_x_co_ord.remove(self)
            #listOfEnemies.remove(self)
            #self.activity = DYING
        

class FlyingEnemy(Enemy):
    
    
    sprites = []
    width_of_enemy = 100
    height_of_enemy = 100
    
    spawn = USEREVENT + 1
    updateImgEvent = USEREVENT + 2
    attack_range = 20
    attack_damage = 20

    sprites.append(pygame.image.load('alien-enemy-flying1.png'))
    sprites.append(pygame.image.load('alien-enemy-flying2.png'))
    sprites.append(pygame.image.load('alien-enemy-flying3.png'))
    sprites.append(pygame.image.load('alien-enemy-flying4.png'))
    sprites.append(pygame.image.load('alien-enemy-flying5.png'))
    sprites.append(pygame.image.load('alien-enemy-flying6.png'))
    sprites.append(pygame.image.load('alien-enemy-flying7.png'))
    sprites.append(pygame.image.load('alien-enemy-flying8.png'))

    current_sprite = 0
    image = sprites[0]

    def __init__(self, that_games_resource_system):
        
        self.rect = pygame.Rect(GAME_RECT.right, floor_level, self.width_of_enemy, self.height_of_enemy)
        self.rect.bottom = floor_level + 5
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.activity = 'advancing'
        self.health = 200
        self.resource_system = that_games_resource_system
        
        pygame.time.set_timer(self.updateImgEvent, 75)


    def updateImage(self):
        if self.activity == DYING:
            self.kill()
        

        elif self.current_sprite >= 7:
                self.current_sprite = 0
        else:
            self.current_sprite += 1
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)


        
class WalkingEnemy(Enemy):
    
    rows = 1
    columns = 6
    sprites = []
    sprite_width = 57
    sprite_height = 42
    width_of_enemy = 100
    height_of_enemy = 100
    attack_range = 75
    attack_damage = 40
    
    spawn = USEREVENT + 1
    updateImgEvent = USEREVENT + 2

    extractSprites(1, 6, sprite_width, sprite_height, sprites, 'alien-enemy-walk.png', width_of_enemy, height_of_enemy) # 0 to 5 are walking
    extractSprites(1, 4, 48, 48, sprites, 'alien-enemy-idle.png', width_of_enemy, height_of_enemy) # 6 to 9 are idling

    current_sprite = 0
    image = sprites[0]

    def __init__(self, that_games_resource_system ):
        
        self.rect = pygame.Rect(GAME_RECT.right, floor_level, self.width_of_enemy, self.height_of_enemy)
        self.rect.bottom = floor_level + 10
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.health = 300
        self.resource_system = that_games_resource_system
        self.activity = ADVANCING
        pygame.time.set_timer(self.updateImgEvent, 75)

    def updateImage(self):
        if self.activity == ADVANCING:

            if self.current_sprite >= 5:
                    self.current_sprite = 0
            else:
                self.current_sprite += 1
        elif self.activity == ATTACKING:
            if self.current_sprite >= 9 or self.current_sprite < 6:
                self.current_sprite = 6
            else:
                self.current_sprite += 1
        else:
            self.current_sprite = 6
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)


class DogEnemy(Enemy):
    
    
    sprites = []
    width_of_enemy = 128
    height_of_enemy = 64
    width_of_enemy = 300
    height_of_enemy = 300
    
    spawn = USEREVENT + 1
    updateImgEvent = USEREVENT + 2
    

    extractSprites(1, 8, 150, 150, sprites, 'run.png', width_of_enemy, height_of_enemy)

    for sprite in sprites:
        sprite = pygame.transform.flip(sprite, True, False)
    
    image = sprites[0]

    def __init__(self, that_games_resource_system):
        self.speed = 4
        self.current_sprite = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(GAME_RECT.right, floor_level, self.width_of_enemy, self.height_of_enemy)
        self.rect.bottom = floor_level + 100
        self.image = self.sprites[0]   
        self.shooting = False
        self.activity = 'advancing'
        self.health = 100
        self.resource_system = that_games_resource_system
        self.mask_height, self.mask_width = self.mask.get_size()
        pygame.time.set_timer(self.updateImgEvent, 75)


    def updateImage(self):
        if self.activity == DYING:
            self.kill()
        

        elif self.current_sprite >= 4:
                self.current_sprite = 0
        else:
            self.current_sprite += 1
        self.image = pygame.transform.flip(self.sprites[self.current_sprite], True, False)
        pygame.time.set_timer(self.updateImgEvent, 75)


class EnemyTotem(Enemy):
    speed = 0
    sprites = []
    updateImgEvent = USEREVENT + 2

    extractSprites(1, 11, 100, 140, sprites, 'red_moon_tower.png', 200, 280)

    current_sprite = 0
    attack_range = 0
    

    def __init__(self, that_games_resource_system):
        self.rect = pygame.Rect(3500, 350, 100, 140)
        self.health = 10000
        self.image = self.sprites[self.current_sprite]
        self.shooting = False
        self.resource_system = that_games_resource_system
        

    def updateImage(self):
        if self.current_sprite == 10:
            self.current_sprite = 0
        else: 
            self.current_sprite += 1
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)



class Drill():
    global listOfBuildings
    metal_produced_per_second = 20

    metal_building_cost = 100
    uranium_building_cost = 100
    energy_building_cost = 0
    width_of_sprite = 60
    height_of_sprite = 90


    def __init__(self, resource_system):
        self.rect = pygame.Rect(GAME_RECT.left + 900, floor_level, self.width_of_sprite, self.height_of_sprite)
        self.rect.bottom = floor_level + 5
        self.image = pygame.transform.scale(pygame.image.load('drill.png'), (60, 90))
        self.mask = pygame.mask.from_surface(self.image)
        self.resource_system = resource_system
        
        if len(listOfBuildings) >= 1:
            self.rect.centerx = listOfBuildings[-1].rect.centerx + distance_between_building_centroids
        else:
            self.rect.centerx = GAME_RECT.left + 200


    def produceRelevantResource(self):
        self.resource_system.change_Metal_Level(Drill.metal_produced_per_second)

class Reactor(): 
    global listOfBuildings
    energy_produced_per_second = 10 # the reactor turns uranium into energy at this rate
    uranium_cost_per_second = 10

    metal_building_cost = 500
    uranium_building_cost = 200
    energy_building_cost = 0
    width_of_sprite = 60
    height_of_sprite = 90
    

    def __init__(self, resource_system):
        self.rect = pygame.Rect(GAME_RECT.left + 900, floor_level, self.width_of_sprite, self.height_of_sprite)
        self.rect.bottom = floor_level + 5
        self.image = pygame.transform.scale(pygame.image.load('energy-station1.png'), (60, 90))
        self.mask = pygame.mask.from_surface(self.image)
        self.resource_system = resource_system

        if len(listOfBuildings) >= 1:
            self.rect.centerx = listOfBuildings[-1].rect.centerx + distance_between_building_centroids
        else:
            self.rect.centerx = GAME_RECT.left + 200

    def produceRelevantResource(self):
        if self.resource_system.uranium_level >= 10:
            self.resource_system.change_Energy_Level(Reactor.energy_produced_per_second)
            self.resource_system.change_Uranium_Level(-Reactor.uranium_cost_per_second)

class Lab():
    global listOfBuildings
    research_produced_per_second = 1

    metal_building_cost = 500
    uranium_building_cost = 250
    energy_building_cost = 750

    width_of_sprite = 80
    height_of_sprite = 90


    def __init__(self, resource_system):
        self.rect = pygame.Rect(GAME_RECT.left + 900, floor_level, self.width_of_sprite, self.height_of_sprite)
        self.rect.bottom = floor_level + 5
        self.image = pygame.transform.scale(pygame.image.load('trading_hut.png'), (80, 90))
        self.mask = pygame.mask.from_surface(self.image)
        self.resource_system = resource_system

        if len(listOfBuildings) >= 1:
            self.rect.centerx = listOfBuildings[-1].rect.centerx + distance_between_building_centroids
        else:
            self.rect.centerx = GAME_RECT.left + 200

    def produceRelevantResource(self):
        self.resource_system.change_Research_Level(self.research_produced_per_second)
        

class WaveOfEnemies():
    global listOfEnemies#, listOfWaves

    
    startWaveEvent = USEREVENT + 5

    def __init__(self, no_of_flys, no_of_walking, no_of_dog, the_games_resource_system):
        self.list_of_flying_aliens_in_the_wave = [FlyingEnemy(the_games_resource_system) for i in range(no_of_flys)]
        self.list_of_walking_aliens_in_the_wave = [WalkingEnemy(the_games_resource_system) for i in range(no_of_walking)]
        self.list_of_dog_aliens_in_the_wave = [DogEnemy(the_games_resource_system) for i in range(no_of_dog)]
        self.the_games_resource_system = the_games_resource_system
        # listOfWaves.append(self)
        

    def startWave(self):
        global listOfEnemies
        x_offset = 0
        for flyingEnemy in self.list_of_flying_aliens_in_the_wave:
            flyingEnemy.rect.x += x_offset
            flyingEnemy.resource_system = self.the_games_resource_system
            listOfEnemies.append(flyingEnemy)
            x_offset += 80
        
        for walkingEnemy in self.list_of_walking_aliens_in_the_wave:
            walkingEnemy.rect.x += x_offset
            walkingEnemy.resource_system = self.the_games_resource_system
            listOfEnemies.append(walkingEnemy)
            x_offset += 80

        for dogEnemy in self.list_of_dog_aliens_in_the_wave:
            dogEnemy.rect.x += x_offset
            dogEnemy.resource_system = self.the_games_resource_system
            listOfEnemies.append(dogEnemy)
            x_offset += 80
        
class Tank(Troop):
    global listOfTanks, listOfTroops

    sprites = []

    width_of_tank = 198
    height_of_tank = 108



    attack_range = 300
    attack_damage = 10000
    health = 1000

    metal_cost = 400
    energy_cost = 100
    
    updateImgEvent = USEREVENT + 2
    purchase_cooldown_over = USEREVENT + 3
    purchase_cooldown_active = False
    
    advancing_sprite_sheet = SpriteSheet('tank_advancing.png')
   
    list_of_scaled_sprites = []
    list_of_running_sprites = advancing_sprite_sheet.load_grid_images(1, 4, 10, 20, 0, 0)
    
# 165 x 90
    for sprite in list_of_running_sprites:
        scaled_sprite = pygame.transform.scale(sprite, (width_of_tank, height_of_tank))
        list_of_scaled_sprites.append(scaled_sprite)
        
    sprites.extend(list_of_scaled_sprites)
    current_sprite = 0
    image = sprites[0]
    

    def __init__(self, resource_system):
        
        self.rect = pygame.Rect(GAME_RECT.left + 20, floor_level, self.width_of_tank, self.height_of_tank)
        self.rect.bottom = floor_level
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.enemy_in_range = False
        
        self.resource_system = resource_system
        self.resource_system.metal_level -= Wizard.metal_cost
        self.resource_system.energy_level -= Wizard.energy_cost
        self.attack_due = self.enemy_in_range
        listOfTanks.append(self)
        
        pygame.time.set_timer(self.updateImgEvent, 75)
    
    def updateImage(self):
        # if self.shooting == True:
        if self.activity == ATTACKING:
            self.current_sprite = 1
            


        elif self.activity == ADVANCING:
            if self.current_sprite >= 3:
                    self.current_sprite = 0
            else:
                self.current_sprite += 1

        elif self.activity == IDLING:
            self.current_sprite = 1
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)

    def check_If_Dying(self):
        if self.health <= 0:
            listOfTroops.remove(self)
            listOfTanks.remove(self)
            del(self)


class Bullet(pygame.sprite.Sprite): # needs a rect to store location, update function, image, advance function to update location, init function to take in troop firing as paramater
    global listOfExplosions, listOfBullets
    speed = 50
    num_bullets = 0

    sprite_width = 11 # the bullet images are 11 x 4 in the sprite sheet
    sprite_height = 4

    bullet_width = 11 # these are the dimensions that I want the bullet to have in the game
    bullet_height = 4

    sprites = []
    
    # to check bullet collisons with enemy, i can have a nested for loop which loops through all bullets and all enemies adn checks for collisons, 
    # if there is a collion (using masks): calls the bulletimpact method on the bullet that hit him which takes in the enemy_hit as an argument
    # the method will then remove the bullet.troop_that_fired_me.damage from the enemy_hit.health delete the bullet object, and 

    extractSprites(1, 2, sprite_width, sprite_height, sprites, 'bullet.png', bullet_width, bullet_height)
    tank_bullet_sprites = []
    for i in range(len(sprites)):
        tank_bullet_sprites.append(pygame.transform.scale(sprites[i], (20,10)))

    image = sprites[0]

    def __init__(self, troop_firing_the_bullet: Troop):
        Bullet.num_bullets += 1
        troop_rect = troop_firing_the_bullet.rect
        class_attributes_of_troop_that_fired = type(troop_firing_the_bullet).__dict__
        if isinstance(troop_firing_the_bullet, Tank):
            self.rect = pygame.Rect(troop_rect.right - 60, troop_rect.top + 45, self.bullet_width * 2, self.bullet_height * 2)
            self.image = self.tank_bullet_sprites[0]
        else:
            self.rect = pygame.Rect(troop_rect.right, troop_rect.top + 45, self.bullet_width, self.bullet_height) # to adapt this to other types fo troop other than infantry, im going to need to have an if statment e.g if troop_firing: type == lightinfanttry: then construct the rect with this y value (which will corrospond to the height of the gun) needed for each troop type 
            self.image = self.sprites[0]

        #self.troop_that_fired_me = troop_firing_the_bullet
        self.type_of_troop_that_fired_me = type(troop_firing_the_bullet)
        self.damage_of_this_bullet = class_attributes_of_troop_that_fired['attack_damage']
        self.mask = pygame.mask.from_surface(self.image)


    def updateImage(self):
        if self.type_of_troop_that_fired_me == Tank:
            if self.image == self.tank_bullet_sprites[0]:
                self.image = self.tank_bullet_sprites[1]
            else:
                self.image = self.tank_bullet_sprites[0]

        else:
            if self.image == self.sprites[0]:
                self.image = self.sprites[1]
            else:
                self.image = self.sprites[0]


    def advance(self):
        self.rect.x += self.speed

    def bulletImpact(self, enemy_hit: Enemy):
        if self.type_of_troop_that_fired_me == Tank:
            listOfExplosions.append(Explosion(self, enemy_hit))
        
        enemy_hit.health -= self.damage_of_this_bullet
        if self in listOfBullets:
            listOfBullets.remove(self)

        del(self)
        Bullet.num_bullets -= 1
        

class ResourceSystem():


    def __init__(self):
        self.metal_level = 9999
        self.uranium_level = 9999
        self.energy_level = 9999
        self.research_level = 0
        self.number_of_troops = 0

    def change_Uranium_Level(self, change):
        self.uranium_level += change
    
    def change_Metal_Level(self, change):
        self.metal_level += change

    def change_Energy_Level(self, change):
        self.energy_level += change

    def change_Research_Level(self, change):
        self.research_level += change

class Knight(Troop): 

    sprites = []

    width_of_knight = 38 * 3
    height_of_knight = 27 * 3


    attack_range = 300
    attack_damage = 2

    metal_cost = 400
    energy_cost = 100
    
    updateImgEvent = USEREVENT + 2
    purchase_cooldown_over = USEREVENT + 3
    purchase_cooldown_active = False
    
    advancing_sprite_sheet = SpriteSheet('knight_running.png')
    attacking_sprite_sheet = SpriteSheet('knight_attack2.png')
    
   
    list_of_scaled_sprites = []
    list_of_running_sprites = advancing_sprite_sheet.load_grid_images(1, 6, 19, 38, 0, 0) # 0-5 are running
    list_of_attacking_sprites = attacking_sprite_sheet.load_grid_images(1, 12, 5, 20, 2, 0) # 6-17 are attacking

    

    for sprite in list_of_running_sprites:
        scaled_sprite = pygame.transform.scale(sprite, (width_of_knight, height_of_knight))
        list_of_scaled_sprites.append(scaled_sprite)
    for sprite in list_of_attacking_sprites:
        scaled_sprite = pygame.transform.scale(sprite, (width_of_knight * 2, height_of_knight * 2))
        list_of_scaled_sprites.append(scaled_sprite)
        
    sprites.extend(list_of_scaled_sprites)
    current_sprite = 0
    image = sprites[0]
    

    def __init__(self, resource_system):
        
        self.rect = pygame.Rect(GAME_RECT.left + 20, floor_level, self.width_of_knight, self.height_of_knight)
        self.rect.bottom = floor_level + 5
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.enemy_in_range = False
        self.health = 100
        self.resource_system = resource_system
        self.resource_system.metal_level -= Wizard.metal_cost
        self.resource_system.energy_level -= Wizard.energy_cost
        self.attack_due = self.enemy_in_range
        
        pygame.time.set_timer(self.updateImgEvent, 75)
    
    def updateImage(self):
        # if self.shooting == True:
        if self.activity == ATTACKING:
            if self.current_sprite < 6 or self.current_sprite >= 17:
                self.current_sprite = 6
            else:
                self.current_sprite += 1

        elif self.activity == ADVANCING:
            if self.current_sprite >= 5:
                    self.current_sprite = 0
            else:
                self.current_sprite += 1

        elif self.activity == IDLING:
            self.current_sprite = 1
        self.image = self.sprites[self.current_sprite]
        pygame.time.set_timer(self.updateImgEvent, 75)

class Explosion(pygame.sprite.Sprite):
    sprites = []
    
    # extractSprites(1, 9, 100, 110, sprites, 'explosion-animation.png', 115, 110)

    advancing_sprite_sheet = SpriteSheet('explosion-animation.png')
   
    list_of_scaled_sprites = []
    list_of_running_sprites = advancing_sprite_sheet.load_grid_images(1, 9, 0, 0, 0, 0)

    

    for sprite in list_of_running_sprites:
        scaled_sprite = pygame.transform.scale(sprite, (115, 110))
        list_of_scaled_sprites.append(scaled_sprite)
        
    sprites.extend(list_of_scaled_sprites)
    

    def __init__(self, bullet_that_caused_the_explosion, enemy_hit_by_that_bullet):
        
        self.rect = pygame.Rect(enemy_hit_by_that_bullet.rect.x, enemy_hit_by_that_bullet.rect.top - 25, 115, 100)
        self.current_sprite = 0
        self.image = self.sprites[0]


    def updateImage(self):
        if self.image == self.sprites[8]:
            listOfExplosions.remove(self)
            del self
        else:
            self.current_sprite += 1
            self.image = self.sprites[self.current_sprite]
        


