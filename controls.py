import pygame.font
from settings import *


class ControlsMenu:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.bigfont = pygame.font.Font(BIG_FONT, 65)
        self.font = pygame.font.Font(FONT, 25)
        self.window = pygame.image.load("pictures/ui/box.png").convert_alpha()
        self.window_rect = self.window.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.title = self.bigfont.render("Controls", False, FONT_COLOR)
        self.title_rect = self.title.get_rect(center=(self.window_rect.centerx, self.window_rect.top + 120))
        self.pic = pygame.image.load("pictures/ui/controls.png").convert_alpha()
        self.pic_rect = self.pic.get_rect(topleft=self.window_rect.topleft + pygame.math.Vector2(80, 160))
        self.list = ["move", "swap weapon", "swap spell", "use spell", "close/menu", "use weapon", "player stats"]
        self.texts = []
        self.text_rects = []
        for id, item in enumerate(self.list):
            text = self.font.render("-    " + item, False, FONT_COLOR)
            self.texts.append(text)
            if id < 4:
                text_rect = text.get_rect(topleft=self.window_rect.topleft + pygame.math.Vector2(240, 230 + id * 93))
                self.text_rects.append(text_rect)
            else:
                text_rect = text.get_rect(topleft=self.window_rect.topleft + pygame.math.Vector2(640, 230 + (id - 4) * 93))
                self.text_rects.append(text_rect)

    def display(self):
        self.screen.blit(self.window, self.window_rect)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.pic, self.pic_rect)
        for id, text in enumerate(self.texts):
            self.screen.blit(text, self.text_rects[id])
