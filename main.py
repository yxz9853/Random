import pygame, sys
from settings import *
from settings import level_map
from level import Level
from button import Button
import support
import player
import shutil
import time
pygame.init()

screen=pygame.display.set_mode((1366,768))
pygame.display.set_caption("Menu")
bg=pygame.image.load("./graphics/background/background.jpg")
gbg=pygame.image.load("./graphics/background/index.jpg")
gbg=pygame.transform.scale(gbg,(1366,768))

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    while True:
        pygame.display.set_caption('Main Menu')
        screen.blit(bg, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Random", True, "#000000")
        menu_rect = menu_text.get_rect(center=(683, 150))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(683, 350),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        controls_button = Button(image=pygame.image.load("assets/Controls Rect.png"), pos=(683, 480),
                            text_input="CONTROLS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(683, 610),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, quit_button, controls_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    while support.restart==True:
                        support.restart=False
                        support.ref=int(time.time())
                        generate()
                        play()

                    support.timed=int(time.time())-support.ref
                    end()
                    support.restart=True
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if controls_button.checkForInput(menu_mouse_pos):\
                    controls()
        pygame.display.update()

def play():
    support.restart=False
    support.lost=0
    pygame.display.set_caption('Random')
    screen.blit(gbg, (0,0))
    clock=pygame.time.Clock()
    level=Level(generate(),screen)
    support.bgx=0
    while True and support.lost==0 and support.restart==False:
        menu_mouse_pos=pygame.mouse.get_pos()

        screen.fill('black')
        for i in range(0,25):
            screen.blit(gbg, (support.bgx+1366*i,0))
        screen.blit(gbg, (support.bgx,0))
        screen.blit(gbg, (support.bgx-1366,0))
        screen.blit(gbg, (support.bgx+1366,0))

        restart_button = Button(image=pygame.image.load("assets/Controls Rect.png"), pos=(300, 110),
                            text_input="RESTART", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

        for button in [restart_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.checkForInput(menu_mouse_pos):
                    support.restart=True

        level.run()

        pygame.display.update()
        clock.tick(60)

def end():
    pygame.display.set_caption('Game Over')
    if support.lost==1:
        while True:
            menu_mouse_pos=pygame.mouse.get_pos()
            restart_button = Button(image=pygame.image.load("assets/Controls Rect.png"), pos=(300, 110),
                            text_input="RESTART", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

            screen.fill('black')
            game_text = get_font(200).render("GAME", True, "#b68f40")
            game_rect = game_text.get_rect(center=(683, 270))
            over_text = get_font(200).render("OVER", True, "#b68f40")
            over_rect = over_text.get_rect(center=(683, 530))

            screen.blit(game_text, game_rect)
            screen.blit(over_text, over_rect)

            for button in [restart_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.checkForInput(menu_mouse_pos):
                        return
            pygame.display.update()

    elif support.lost==-1:
        while True:
            menu_mouse_pos=pygame.mouse.get_pos()
            restart_button = Button(image=pygame.image.load("assets/Controls Rect.png"), pos=(300, 110),
                            text_input="RESTART", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

            screen.fill('yellow')

            you_text = get_font(200).render("YOU", True, "#b68f40")
            you_rect = you_text.get_rect(center=(683, 270))
            win_text = get_font(200).render("WIN", True, "#b68f40")
            win_rect = win_text.get_rect(center=(683, 530))
            time_text = get_font(50).render(str(support.timed), True, "#b68f40")
            time_rect = time_text.get_rect(center=(930,75))
            seconds_text = get_font(50).render("seconds", True, "#b68f40")
            seconds_rect = seconds_text.get_rect(topleft=(930+len(str(support.timed))*40-len(str(support.timed))*10, 50))

            screen.blit(you_text, you_rect)
            screen.blit(win_text, win_rect)
            screen.blit(time_text, time_rect)
            screen.blit(seconds_text, seconds_rect)
            for button in [restart_button]:
                button.changeColor(menu_mouse_pos)
                button.update(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.checkForInput(menu_mouse_pos):
                        return
            pygame.display.update()

def controls():
    pygame.display.set_caption('Controls')
    while True:
        screen.blit(bg, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        controls_text = get_font(100).render("Controls", True, "#000000")
        controls_rect = controls_text.get_rect(center=(683, 150))
        jump_text = get_font(40).render("W or ↑ to jump", True, "#000000")
        jump_rect = jump_text.get_rect(center=(683, 290))
        move_text = get_font(40).render("A and D or ← and → to move", True, "#000000")
        move_rect = move_text.get_rect(center=(683, 390))
        restart_text = get_font(40).render("R to restart", True, "#000000")
        restart_rect = restart_text.get_rect(center=(683, 490))


        back_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(683, 650),
                            text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(controls_text, controls_rect)
        screen.blit(jump_text, jump_rect)
        screen.blit(move_text, move_rect)
        screen.blit(restart_text, restart_rect)

        for button in [back_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(menu_mouse_pos):
                    return
        pygame.display.update()


main_menu()
