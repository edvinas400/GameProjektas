import pygame.mixer
from settings import *
from button import Button
from level import Level
import sys
import pickle


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load("pictures/background2.png").convert_alpha()
        self.background_rect = self.background.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.title = pygame.image.load("pictures/game.png").convert_alpha()
        self.title_rect = self.title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 250))
        self.button_pic = pygame.image.load("pictures/ui/mainbutton.png").convert_alpha()
        self.buttons = []
        try:
            pickle.load(open("saves/save.pkl", "rb"))
            self.list = ["CONTINUE", "NEW GAME", "CONTROLS", "QUIT"]
            for id, item in enumerate(self.list):
                button = Button(self.button_pic, item, 42, (self.background_rect.centerx, 390 + 130 * id))
                self.buttons.append(button)
        except:
            self.list = ["NEW GAME", "CONTROLS", "QUIT"]
            self.title_rect = self.title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 170))
            for id, item in enumerate(self.list):
                button = Button(self.button_pic, item, 42, (self.background_rect.centerx, 500 + 130 * id))
                self.buttons.append(button)
        self.float_v = self.title_rect.centery


    def display(self, game):
        self.title_rect.centery = self.float_v + float(6, 400)
        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.title, self.title_rect)
        for id, button in enumerate(self.buttons):
            button.update()
            if button.check_click():
                sounds["click"].play()
                if self.list[id] == "NEW GAME":
                    game.level = Level(game, "floor_done")
                    game.started = True
                    town_music()
                elif self.list[id] == "CONTINUE":
                    with open('saves/save.pkl', 'rb') as inp:
                        stage = pickle.load(inp)[7]
                    game.level = Level(game, stage)
                    load(game.level)
                    game.started = True
                    town_music()
                elif self.list[id] == "CONTROLS":
                    game.controls_on = True
                elif self.list[id] == "QUIT":
                    pygame.time.delay(400)
                    pygame.quit()
                    sys.exit()

    def update(self):
        self.__init__()
