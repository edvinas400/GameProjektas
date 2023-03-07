from projectiles import *


class PlayerProjectile(Projectile):
    def __init__(self, spell, caster, groups):
        super().__init__(spell, caster, groups)
        direction = caster.status.split("_")[0]
        self.animation = folder_content(f"pictures/particles/{self.spell}/{direction}")
        self.image = self.animation[int(self.frame_id)]
        if direction == "right":
            self.rect = self.image.get_rect(midleft=caster.rect.midright + pygame.math.Vector2(0, 14))
            self.direction = pygame.math.Vector2(1, 0)
        elif direction == "left":
            self.rect = self.image.get_rect(midright=caster.rect.midleft + pygame.math.Vector2(0, 14))
            self.direction = pygame.math.Vector2(-1, 0)
        elif direction == "up":
            self.rect = self.image.get_rect(midbottom=caster.rect.midtop + pygame.math.Vector2(-15, 0))
            self.direction = pygame.math.Vector2(0, -1)
        else:
            self.rect = self.image.get_rect(midtop=caster.rect.midbottom + pygame.math.Vector2(-8, 0))
            self.direction = pygame.math.Vector2(0, 1)
        self.hitbox = self.rect
