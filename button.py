from settings import *


class Button:
    def __init__(self, image, text, font_size, position):
        self.screen = pygame.display.get_surface()
        self.can_press = True
        self.press_time = None
        self.press_cd = 400
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.font = pygame.font.Font(FONT, font_size)
        self.words = text
        self.text = self.font.render(text, False, FONT_COLOR)
        if text != "+":
            self.text_rect = self.text.get_rect(center=position - pygame.math.Vector2(0, 10))
        else:
            self.text_rect = self.text.get_rect(center=position - pygame.math.Vector2(-2, 5))

    def check_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.text = self.font.render(self.words, False, "#e67300")
        else:
            self.text = self.font.render(self.words, False, FONT_COLOR)

        if self.can_press:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.can_press = False
                self.press_time = pygame.time.get_ticks()
                return True

    def cooldown(self):
        now = pygame.time.get_ticks()
        if not self.can_press:
            if now - self.press_time >= self.press_cd:
                self.can_press = True

    def update(self):
        self.cooldown()
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)
