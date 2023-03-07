import math
from settings import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.type = "weapon"
        direction = player.status.split("_")[0]
        path = f"pictures/weapons/{player.weapon}/{direction}.png"
        self.image = pygame.image.load(path).convert_alpha()
        if direction == "right":
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 14))
        elif direction == "left":
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 14))
        elif direction == "up":
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-15, 0))
        else:
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-8, 0))
        self.hitbox = self.rect

    def flicker(self):
        if not self.player.vulnerable:
            value = math.sin(pygame.time.get_ticks())
            if value >= 0:
                alpha = 255
            else:
                alpha = 0
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.flicker()
        if not self.player:
            self.kill()
