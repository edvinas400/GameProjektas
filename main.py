import sys
from settings import *
from main_menu import MainMenu
from controls import ControlsMenu


class Game:
    def __init__(self):
        pygame.init()
        menu_music()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.cursor_img = pygame.image.load("pictures/cursor.png").convert_alpha()
        self.cursor_img_rect = self.cursor_img.get_rect()
        self.clock = pygame.time.Clock()
        self.level = None
        self.menu = MainMenu()
        self.controls_on = False
        self.controls = ControlsMenu()
        self.started = False
        surface = pygame.image.load("pictures/player2/face2.png")
        pygame.display.set_icon(surface)
        pygame.display.set_caption(" MY GAME")

    def run(self):
        while True:
            self.cursor_img_rect.topleft = pygame.mouse.get_pos()
            if not self.started:
                self.menu.display(self)
            else:
                if self.level:
                    self.level.run()
            if self.controls_on:
                self.controls.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.controls_on = False
                if self.started and self.level.player.alive():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.level.levelup_menu()
                        if event.key == pygame.K_ESCAPE:
                            self.level.escape()
            self.screen.blit(self.cursor_img, self.cursor_img_rect)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
