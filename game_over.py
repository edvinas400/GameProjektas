from settings import *
from menu import Menu
from button import Button
from sounds import *



class GameOver(Menu):
    def __init__(self, level):
        super().__init__(level)
        self.title = pygame.image.load("pictures/gameover2.png").convert_alpha()
        self.title_rect = self.title.get_rect(center=(self.window_rect.centerx, self.window_rect.top + 200))
        self.float_v = self.title_rect.centery
        self.buttons = []
        self.button_pic = pygame.image.load("pictures/ui/mainbutton2.png").convert_alpha()
        try:
            pickle.load(open("saves/save.pkl", "rb"))
            self.list = ["load  last  save", "main  menu"]
            for id, item in enumerate(self.list):
                button = Button(self.button_pic, item, 35, (self.window_rect.centerx, 580 + 110 * id))
                self.buttons.append(button)
        except:
            self.list = ["main  menu"]
            for id, item in enumerate(self.list):
                button = Button(self.button_pic, item, 35, (self.window_rect.centerx, 600 + 110 * id))
                self.buttons.append(button)

    def display(self, level):
        self.title_rect.centery = self.float_v + float(6, 400)
        self.screen.blit(self.title, self.title_rect)
        level.game.cursor_img.set_alpha(255)
        for id, button in enumerate(self.buttons):
            button.update()
            if button.check_click():
                sounds["click"].play()
                if self.list[id] == "main  menu":
                    level.game.started = False
                    del level
                    pygame.time.delay(300)
                    menu_music()
                elif self.list[id] == "load  last  save":
                    level.stage = load(level)
                    level.update()
                    load(level)
                    pygame.time.delay(700)
                    town_music()

    def update(self):
        self.__init__(self.level)
