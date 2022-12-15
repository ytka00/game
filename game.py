import pygame
import sys
import math
import os
import random
import time

pygame.init()
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 360

CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Travelling in Ukraine")

#game variables
font = pygame.font.Font('freesansbold.ttf', 20)
scroll = 0
game_speed = 0
count = 0
speed = 50
points = 0
rand = random.randint(0,1)

def main():
#load image
    bg = pygame.image.load("assets/bg1.jpg").convert()
    
    X_POSITION, Y_POSITION = 150, 300

    STANDING_SURFACE = pygame.transform.scale(pygame.image.load("assets/tractor.png"), (300,110))
    JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("assets/tractor.png"), (250, 110))
    WITH_TANK = pygame.transform.scale(pygame.image.load("assets/tank.png"), (300,110))
    JUMPING_TANK = pygame.transform.scale(pygame.image.load("assets/tank.png"), (250,110))
    WITH_TANK2 = pygame.transform.scale(pygame.image.load("assets/tank2.png"),(300,110))
    JUMPING_TANK2 = pygame.transform.scale(pygame.image.load("assets/tank2.png"),(300,110))
    mario_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
#akadályok
    HAY = pygame.transform.scale(pygame.image.load("assets/hay.png"), (90,60))
    O_TANK = pygame.transform.scale(pygame.image.load("assets/o_tank.png"), (90,80))
    
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()
    o_width = HAY.get_width()
    o_rect = HAY.get_rect()

#global variablas
    scroll = 0
    rand = random.randint(0,1)
    game_speed = 0
    count = 0
    death_count = 0
    tiles = math.ceil(SCREEN_WIDTH  / bg_width) + 1
    o_tiles = math.ceil(SCREEN_WIDTH  / o_width) + 1
    
#booleans
    jumping = False
    tank = False
    tank2 = False
    o_tank = False
    
    Y_GRAVITY = 0.5
    JUMP_HEIGHT = 16
    Y_VELOCITY = JUMP_HEIGHT

    def score():
        global speed, points
        points += pow(count,count)+1
        if points % 100 == 0:
            speed += 1

        text = font.render("Танки: " + str(count) + " Точки: " + str(points//10), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)

#run game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
                jumping = True
        if keys_pressed[pygame.K_w]:
            if count > 0:
                count = 0
                tank = False
                tank2 = False
    
        screen.blit(bg, (0, 0))
        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll
        if rand == 1:
            for i in range(0, o_tiles):
                screen.blit(HAY, (1400 + game_speed, 290))
                o_rect.x = i * o_width + game_speed
        else:
            o_tank = True
            for i in range(0, o_tiles):
                screen.blit(O_TANK, (1400 + game_speed, 270))
                o_rect.x = i * o_width + game_speed
        scroll -= 4
        game_speed -= 4
        if abs(scroll) > bg_width:
            scroll = 0
        if abs(game_speed) > bg_width+200 and not o_tank:
            game_speed = 0
            rand = random.randint(0,1)
        elif abs(game_speed) > bg_width+50 and o_tank:
            game_speed = 0
            rand = random.randint(0,1)
            o_tank = False
            count += 1

        if count > 1:
            tank = False
            tank2 = True
        elif count == 1:
            tank2 = False
            tank = True
        elif count == 0:
            tank = False
            tank2 = False

        if abs(game_speed) < bg_width+50 and abs(game_speed) > bg_width-150:
            if not jumping:
                death_count += 1
                menu(death_count)                
            elif (tank or tank2) and not o_tank:
                death_count += 1
                menu(death_count)

        if jumping:
            Y_POSITION -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY
            if Y_VELOCITY < -JUMP_HEIGHT:
                jumping = False
                Y_VELOCITY = JUMP_HEIGHT
            if tank2:
                mario_rect = JUMPING_TANK2.get_rect(center=(X_POSITION, Y_POSITION))
                screen.blit(JUMPING_TANK2, mario_rect)
            elif tank:
                mario_rect = JUMPING_TANK.get_rect(center=(X_POSITION, Y_POSITION))
                screen.blit(JUMPING_TANK, mario_rect)
            else:
                mario_rect = JUMPING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
                screen.blit(JUMPING_SURFACE, mario_rect)
        elif tank2:
            mario_rect = WITH_TANK2.get_rect(center=(X_POSITION, Y_POSITION))
            screen.blit(WITH_TANK2, mario_rect)
        elif tank:
            mario_rect = WITH_TANK.get_rect(center=(X_POSITION, Y_POSITION))
            screen.blit(WITH_TANK, mario_rect)
        else:
            mario_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
            screen.blit(STANDING_SURFACE, mario_rect)
    
        score()
        pygame.display.update()
        CLOCK.tick(speed)

def menu(death_count):
    global points
    run = True
    menu_bg = pygame.image.load("assets/menu.png").convert()
    menu_width = menu_bg.get_width()
    menu_rect = menu_bg.get_rect()
    screen.blit(menu_bg, (0,0))
    def help():
        run2 = True
        while run2:
            help_bg = pygame.image.load("assets/help.png").convert()
            screen.blit(help_bg, (0,0))
            keys_pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    points = 0
                    main()
                    run2 = False
            pygame.display.update()

    while run:
        if death_count == 0:
            title = font.render("поездка по Украине", True, (255, 255, 255))
            text = font.render("Нажмите любую кнопку, чтобы начать", True, (255, 255, 255))
            titleRect = title.get_rect()
            titleRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130 )
            screen.blit(title, titleRect)
        elif death_count > 0:
            text = font.render("Нажмите любую кнопку, чтобы перезапустить", True, (255, 255, 255))
            score = font.render("Точки: " + str(points//10),True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130)
            screen.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80 )
        screen.blit(text, textRect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_h:
                    help()
                else:
                    points = 0
                    main()
                    
death_count = 0
menu(death_count)
