import pygame
import pygame_menu
import sys
import time
import random
from pygame.locals import *
import subprocess as sp
width = 500
pygame.init()
pygame.display.set_caption("Snake")
pygame.mixer.music.load("sounds/pop.wav")
window = pygame.display.set_mode((width, width))
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
lightblue = pygame.Color(173,216,230)
snake_pos = [100, 50]
direction = 'RIGHT'
change_to = direction
clock = pygame.time.Clock()
global score
difficulty = 10
def start_game():
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    clock = pygame.time.Clock()
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (width // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    global score
    score = 0
    difficulty = 10
    global hp_counter
    hp_counter = 3
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            difficulty += 1
            pygame.mixer.music.play(0)
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (width // 10)) * 10]
        food_spawn = True

        window.fill(lightblue)
        for pos in snake_body:
            # Snake body
            pygame.draw.rect(window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 0:
            hp_counter -= 1
            snake_pos[0] = width - 10
            if hp_counter == 0:
                game_over()
        if snake_pos[0] > width - 10:
            hp_counter -= 1
            snake_pos[0] = 0
            if hp_counter == 0:
                game_over()
        if snake_pos[1] < 0:
            hp_counter -= 1
            snake_pos[1] = width - 10
            if hp_counter == 0:
                game_over()
        if snake_pos[1] > width - 10:
            hp_counter -= 1
            snake_pos[1] = 0
            #show_hp(1, black, "consolas", 20)
            if hp_counter == 0:
                game_over()
        for body in snake_body[1:]:
            if snake_pos[0] == body[0] and snake_pos[1] == body[1]:
                hp_counter -= 1
                #show_hp(1, black, "consolas", 20)
            if hp_counter == 0:
                game_over()
        show_hp(1, black, "consolas", 20)
        show_score(1, black, 'consolas', 20)
        pygame.display.update()
        clock.tick(difficulty)
def loadImage(name, useColorKey):
    image = pygame.image.load(name)
    image = image.convert()
    if useColorKey is True:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Game Over', True, black)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width // 2, width // 4)
    window.fill((173,216,230))
    snake_pos[0]=0
    snake_pos[1]=0
    direction = ""
    change_to = direction
    window.blit(game_over_surface, game_over_rect)
    show_score(0, black, 'times', 20)
    pygame.display.flip()
    time.sleep(2)
    with open("score.txt", "w") as f:
        f.write(str(score)+"\n")
        f.close()
    menu = pygame_menu.Menu(300, 400, 'Snake',
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add_text_input('Name :', default='Ja')
    menu.add_button('Play', start_game)
    menu.add_button('Scores', scores)
    menu.add_button("AboutMe", aboutme)
    menu.add_button("Help", instruction)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(window)

def show_score(choice, color, font, size):
    pygame.init()
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (width // 10, 15)
    else:
        score_rect.midtop = (width // 2, width // 1.25)
    window.blit(score_surface, score_rect)

def show_hp(choice, color, font, size):
    pygame.init()
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('HP : ' + str(hp_counter), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (width // 10, 35)
    else:
        score_rect.midtop = (width // 2, width // 1.25)
    window.blit(score_surface, score_rect)

def instruction():
    program_name = "notepad.exe"
    file_name = "Help.txt"
    sp.Popen([program_name, file_name])
def aboutme():
    program_name = "notepad.exe"
    file_name = "aboutme.txt"
    sp.Popen([program_name, file_name])
def scores():
    program_name = "notepad.exe"
    file_name = "Score.txt"
    sp.Popen([program_name, file_name])
menu = pygame_menu.Menu(300, 400, 'Snake',
                       theme=pygame_menu.themes.THEME_BLUE)
menu.add_text_input('Name :', default='Ja')
menu.add_button('Play', start_game)
menu.add_button('Scores', scores)
menu.add_button("AboutMe", aboutme)
menu.add_button("Help", instruction)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.mainloop(window)
