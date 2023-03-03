import pygame, sys
from pygame import *
from my_classes import *
pygame.init()


# create resource system, player/enemy totem, and enemy wave objects
myResourceSystem = ResourceSystem()
myWave = WaveOfEnemies(9, 9, 0, myResourceSystem)
myWave.startWave()
player_totem = PlayerTotem()
enemy_totem = EnemyTotem(myResourceSystem)
listOfTroops.append(player_totem)
listOfEnemies.append(enemy_totem)

# main game loop
while True:

    # this code handles the interaction between the sprites (when they get in each others way, when they should attack each other etc)
    listOfTroop_sorted_according_to_x_co_ord = sorted(listOfTroops)
    leading_troop = listOfTroop_sorted_according_to_x_co_ord[-1]
    listOfEnemies_sorted_according_to_x_co_ord = sorted(listOfEnemies)
    leading_enemy = listOfEnemies_sorted_according_to_x_co_ord[-1]


    if leading_troop.rect.right - 40 >= leading_enemy.rect.left:
        leading_troop.blocked = True
        leading_enemy.blocked = True
    else: 
        leading_troop.blocked = False
        leading_enemy.blocked = False

    for i in range(len(listOfEnemies_sorted_according_to_x_co_ord) -1 ): # what this means is that if the enemy in front is blocked and you come close to them, you're blocked too
        if listOfEnemies_sorted_according_to_x_co_ord[i+1].blocked == True and listOfEnemies_sorted_according_to_x_co_ord[i+1].rect.left <= listOfEnemies_sorted_according_to_x_co_ord[i].rect.right:
            listOfEnemies_sorted_according_to_x_co_ord[i].blocked = True
        else:
            listOfEnemies_sorted_according_to_x_co_ord[i].blocked = False

    for i in range(len(listOfTroop_sorted_according_to_x_co_ord) -1 ): # what this means is that if the troop in front is blocked and you come close to them, you're blocked too
        if (listOfTroop_sorted_according_to_x_co_ord[i+1].blocked == True or listOfTroop_sorted_according_to_x_co_ord[i+1].activity == ATTACKING) and listOfTroop_sorted_according_to_x_co_ord[i+1].rect.left <= listOfTroop_sorted_according_to_x_co_ord[i].rect.right:
            listOfTroop_sorted_according_to_x_co_ord[i].blocked = True
        else:
            listOfTroop_sorted_according_to_x_co_ord[i].blocked = False

        if leading_troop.rect.right + leading_troop.attack_range >= leading_enemy.rect.right:
            leading_troop.enemy_in_range = True
            leading_troop.checkCurrentActivity()
        else:
            leading_troop.enemy_in_range = False

    for troop in listOfTroop_sorted_according_to_x_co_ord:
        if troop.rect.right + troop.attack_range >= leading_enemy.rect.right:
            troop.enemy_in_range = True
        

        else:
            troop.enemy_in_range = False
        troop.checkCurrentActivity()

    for enemy in listOfEnemies_sorted_according_to_x_co_ord:
        if enemy.rect.left - enemy.attack_range <= leading_troop.rect.right:
            enemy.enemy_in_range = True
            
        else:
            enemy.enemy_in_range = False
        enemy.checkCurrentActivity()

    if len(listOfEnemies_sorted_according_to_x_co_ord) == 0:
        for troop in listOfTroop_sorted_according_to_x_co_ord:
            troop.enemy_in_range = False
            troop.checkCurrentActivity()


    # scrolling mechanic
    mousePosition = pygame.mouse.get_pos()
    if mousePosition[0] > SCREEN_WIDTH * (9/10) and GAME_RECT.right > 2200:


        for troop in listOfTroops:
            troop.rect.x -= scroll_speed
        for enemy in listOfEnemies:
            enemy.rect.x -= scroll_speed
        for building in listOfBuildings:
            building.rect.x -= scroll_speed
        for explosion in listOfExplosions:
            explosion.rect.x -= scroll_speed
        for bullet in listOfBullets:
            bullet.rect.x -= scroll_speed
        
        user_interface_rect.x -= scroll_speed

        background_building_rect.x -= scroll_speed * .5
        GAME_RECT.x -= scroll_speed * .25


    if mousePosition[0] < SCREEN_WIDTH * (1/10) and GAME_RECT.left < 0:

        for troop in listOfTroops:
            troop.rect.x += scroll_speed
        for enemy in listOfEnemies:
            enemy.rect.x += scroll_speed
        for building in listOfBuildings:
            building.rect.x += scroll_speed
        for explosion in listOfExplosions:
            explosion.rect.x += scroll_speed
        for bullet in listOfBullets:
            bullet.rect.x += scroll_speed

        user_interface_rect.x += scroll_speed

        background_building_rect.x += scroll_speed * .5
        GAME_RECT.x += scroll_speed * .25

    # event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # anything I want to happen every second goes here
        if event.type == one_second_has_passed:
            pygame.time.set_timer(one_second_has_passed, 1000)
            for building in listOfBuildings:
                building.produceRelevantResource()
            for enemy in listOfEnemies_sorted_according_to_x_co_ord:
                if enemy.enemy_in_range == True:
                    leading_troop.health -= enemy.attack_damage

        if event.type == two_seconds_have_passed:
            pygame.time.set_timer(two_seconds_have_passed, 2000)
            for tank in listOfTanks:
                if tank.activity == ATTACKING:
                    listOfBullets.append(Bullet(tank))
            
        
        if event.type == Infantry.updateImgEvent:
            for troop in listOfTroops:
                troop.checkCurrentActivity()
                troop.updateImage()

        if event.type == FlyingEnemy.updateImgEvent:
            for enemy in listOfEnemies:
                enemy.updateImage()

        if event.type == player_totem.updateImgEvent:
            player_totem.updateImage()

        if event.type == enemy_totem.updateImgEvent:
            enemy_totem.updateImage()
        

        # clicking on the screen, e.g to buy a new troop or building
        if event.type == MOUSEBUTTONDOWN:
            if infantry_icon_rect.collidepoint(mousePosition) and Infantry.purchase_cooldown_active == False and myResourceSystem.metal_level >= Infantry.metal_cost and myResourceSystem.energy_level >= Infantry.energy_cost:
                listOfTroops.append(Infantry(myResourceSystem))
                Infantry.purchase_cooldown_active = True
                pygame.time.set_timer(Infantry.purchase_cooldown_over, 1000)

            if light_infantry_icon_rect.collidepoint(mousePosition) and LightInfantry.purchase_cooldown_active == False and myResourceSystem.metal_level >= LightInfantry.metal_cost:
                listOfTroops.append(LightInfantry(myResourceSystem))
                LightInfantry.purchase_cooldown_active = True
                pygame.time.set_timer(LightInfantry.purchase_cooldown_over, 1000)

            if drill_icon_rect.collidepoint(mousePosition):
                listOfBuildings.append(Drill(myResourceSystem))

            if reactor_icon_rect.collidepoint(mousePosition):
                listOfBuildings.append(Reactor(myResourceSystem))

            if lab_icon_rect.collidepoint(mousePosition):
                listOfBuildings.append(Lab(myResourceSystem))

            if wizard_icon_rect.collidepoint(mousePosition) and myResourceSystem.metal_level >= Wizard.metal_cost and myResourceSystem.energy_level >= Wizard.energy_cost:
                listOfTroops.append(Wizard(myResourceSystem))

            if tank_icon_rect.collidepoint(mousePosition):
                listOfTroops.append(Tank(myResourceSystem))

            if knight_icon_rect.collidepoint(mousePosition):
                listOfTroops.append(Knight(myResourceSystem))
            



            

        # limits the rate at which troops can be purchased
        if event.type == Infantry.purchase_cooldown_over:
            Infantry.purchase_cooldown_active = False

        if event.type == LightInfantry.purchase_cooldown_over:
            LightInfantry.purchase_cooldown_active = False
    

    # game_surface
    SCREEN.blit(GAME_SURFACE, GAME_RECT)
    # SCREEN.blit(USER_INTERFACE_SURF, user_interface_rect)

    # far backround layer
    SCREEN.blit(background_building_image, background_building_rect)

    # User interface
    SCREEN.blit(troop_control_icon_image, troop_control_icon_rect) # we have to just blit the UI element directly to SCREEN
    SCREEN.blit(infantry_icon, infantry_icon_rect)
    SCREEN.blit(light_infantry_icon_image, light_infantry_icon_rect)

    SCREEN.blit(knight_icon_image, knight_icon_rect)
    SCREEN.blit(wizard_icon_image, wizard_icon_rect)
    SCREEN.blit(tank_icon_image, tank_icon_rect)

    SCREEN.blit(drill_icon_image, drill_icon_rect)
    SCREEN.blit(reactor_icon_image, reactor_icon_rect)
    SCREEN.blit(lab_icon_image, lab_icon_rect)




    # collision handling between bullets and enemies
    for bullet in listOfBullets:
        for myenemy in listOfEnemies:
            if pygame.sprite.collide_mask(bullet, myenemy):
                bullet.bulletImpact(myenemy)
   


    # handles troop / enemy deaths and their consequences e.g resources dropped from dead enemies
    for myenemy in listOfEnemies_sorted_according_to_x_co_ord:
        myenemy.check_If_Dying()
    for troop in listOfTroop_sorted_according_to_x_co_ord:
        troop.check_If_Dying()



    # prints buildings to the screen
    for building in listOfBuildings:
        SCREEN.blit(building.image, building.rect)
      
    # advances troops and enemies if neccesary and prints them to the screen
    for enemy in listOfEnemies:
        enemy.checkCurrentActivity()
        if enemy.activity == ADVANCING and enemy.blocked == False:
            enemy.advanceForward()
        SCREEN.blit(enemy.image, enemy.rect)

    for troop in listOfTroops:
        troop.checkCurrentActivity()
        if troop.activity == ADVANCING and troop.blocked == False:
            troop.advanceForward()
        SCREEN.blit(troop.image, troop.rect)

    # moves the bullets, changes the animation and blits them to the screen
    for bullet in listOfBullets:
        bullet.advance()
        bullet.updateImage()
        SCREEN.blit(bullet.image, bullet.rect)

    for explosion in listOfExplosions:
        explosion.updateImage()
        SCREEN.blit(explosion.image, explosion.rect)



    # this is the code for the textboxes in the UI that display resource levels, troop numbers and research level
    resource_level_text = ("Metal: {}\n      Uranium: {}\nEnergy: {}".format(myResourceSystem.metal_level, myResourceSystem.uranium_level, myResourceSystem.energy_level))
    lines1 = resource_level_text.splitlines()
    textfont = pygame.font.Font('Pixeltype.ttf', 40)

    y_offset1 = 630
    for line in lines1:
        textbox = textfont.render(line, True, WHITE)
        textbox_rect = textbox.get_rect()
        textbox_rect.center = (1300, y_offset1)
            
        SCREEN.blit(textbox, textbox_rect)
        y_offset1 += 25

    research_and_troop_numbers_text = ("Research: {}\n  Troops: {}/20".format(myResourceSystem.research_level, len(listOfTroops) - 1))
    lines2 = research_and_troop_numbers_text.splitlines()

    y_offset2 = 630
    for line in lines2:
        research_textbox = textfont.render(line, True, WHITE)
        research_textbox_rect = research_textbox.get_rect()
        research_textbox_rect.center = (400, y_offset2)
            
        SCREEN.blit(research_textbox, research_textbox_rect)
        y_offset2 += 35

    # an additional textbox for debugging purposes only
    if len(listOfTroop_sorted_according_to_x_co_ord) >= 1:
        testing_text_box = textfont.render("{},{},{}".format('-', GAME_RECT.left, user_interface_rect) ,True, WHITE)
        testing_text_rect = testing_text_box.get_rect()
        testing_text_rect.center = (200, 200)
        SCREEN.blit(testing_text_box, testing_text_rect)

    # update the screen to reflect the new gamestate and wait for 1/60 of a second (the FPS is 60) to loop through the game loop again
    pygame.display.update()
    fpsClock.tick(FPS)