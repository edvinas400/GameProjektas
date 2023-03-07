from settings import *
from button import Button
from sounds import *


class Menu:
    def __init__(self, level):
        self.level = level
        self.bigfont = pygame.font.Font(BIG_FONT, 85)
        self.button_pic = pygame.image.load("pictures/ui/bigbutton2.png").convert_alpha()
        self.list = ["resume", "save", "controls", "main  menu"]
        self.screen = pygame.display.get_surface()
        self.window = pygame.image.load("pictures/ui/box.png").convert_alpha()
        self.window_rect = self.window.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.title = self.bigfont.render("MENU", False, FONT_COLOR)
        self.title_rect = self.title.get_rect(center=(self.window_rect.centerx, self.window_rect.top + 120))
        self.buttons = []
        for id, item in enumerate(self.list):
            button = Button(self.button_pic, item, 45, (self.window_rect.centerx, 340 + 90 * id))
            self.buttons.append(button)

    def display(self, level):
        self.screen.blit(self.window, self.window_rect)
        self.screen.blit(self.title, self.title_rect)
        for id, button in enumerate(self.buttons):
            button.update()
            if button.check_click():
                sounds["click"].play()
                if self.list[id] == "resume":
                    self.level.menu_window = False
                    self.level.game_paused = False
                elif self.list[id] == "save":
                    save(level)
                    self.level.menu_window = False
                    self.level.game_paused = False
                elif self.list[id] == "controls":
                    self.level.controls_window = True
                    self.level.menu_window = False
                elif self.list[id] == "main  menu":
                    level.game.started = False
                    level.game.menu.update()
                    del level
                    pygame.time.delay(300)
                    menu_music()

