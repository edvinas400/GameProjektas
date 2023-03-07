import pygame.font
from button import *
from settings import *


class LevelUp:
    def __init__(self, player):
        self.screen = pygame.display.get_surface()
        self.player = player
        button_img = pygame.image.load("pictures/ui/button2.png").convert_alpha()
        self.buttons = []
        self.texts = []
        self.text_rects = []
        self.value_rects = []
        self.number_of_attributes = len(player.stats) - 1
        self.attributes = list(player.stats.keys())[:-1]
        self.bigfont = pygame.font.Font("other/gameboy.ttf", 45)
        self.font = pygame.font.Font(FONT, 35)
        self.window = pygame.image.load("pictures/ui/box.png").convert_alpha()
        self.window_rect = self.window.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.title = self.bigfont.render("Player stats", False, FONT_COLOR)
        self.title_rect = self.title.get_rect(midtop=self.window_rect.midtop + pygame.math.Vector2(0, 60))
        points = self.font.render("Points: " + str(self.player.lvlup_points), False, FONT_COLOR)
        self.points_rect = points.get_rect(topleft=self.window_rect.topleft + pygame.math.Vector2(80, 170))
        self.shadow = pygame.image.load("pictures/player2/Shadow.png")
        self.shadow_rect = self.shadow.get_rect(center=self.window_rect.topleft + pygame.math.Vector2(680, 390))
        self.pic = pygame.image.load("pictures/player2/big.png").convert_alpha()
        self.pic_rect = self.pic.get_rect(center=self.window_rect.topleft + pygame.math.Vector2(680, 290))
        for id, attribute in enumerate(self.attributes):
            text = self.font.render(attribute + ":", False, FONT_COLOR)
            text_rect = text.get_rect(topleft=self.window_rect.topleft + pygame.math.Vector2(80, 250 + 40 * id))
            self.texts.append(text)
            self.text_rects.append(text_rect)
            value = self.font.render(str(self.player.stats[attribute]), False, FONT_COLOR)
            value_rect = value.get_rect(topleft=self.window_rect.topleft + pygame.math.Vector2(250, 250 + 40 * id))
            self.value_rects.append(value_rect)
            button = Button(button_img, "+", 30, self.window_rect.topleft + pygame.math.Vector2(320, 275 + 40 * id))
            self.buttons.append(button)

    def display(self):
        font = pygame.font.Font(FONT, 25)
        xp = font.render("XP: " + str(int(self.player.xp)) + "/" + str(int(self.player.stats["max_xp"])), False, FONT_COLOR)
        xp_rect = xp.get_rect(center=self.window_rect.topleft + pygame.math.Vector2(680, 470))
        self.screen.blit(self.window, self.window_rect)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.shadow, self.shadow_rect)
        self.screen.blit(self.pic, self.pic_rect)
        self.screen.blit(xp, xp_rect)
        points = self.font.render("Points: " + str(self.player.lvlup_points), False, FONT_COLOR)
        self.screen.blit(points, self.points_rect)
        for id, text in enumerate(self.texts):
            value = self.font.render(str(self.player.stats[self.attributes[id]]), False, FONT_COLOR)
            self.screen.blit(value, self.value_rects[id])
            self.screen.blit(text, self.text_rects[id])
            if self.player.lvlup_points > 0 and self.player.stats[self.attributes[id]] < self.player.max_stats[self.attributes[id]]:
                self.buttons[id].update()
                if self.buttons[id].check_click():
                    sounds["click"].play()
                    self.player.stats[self.attributes[id]] += 1
                    self.player.lvlup_points -= 1
