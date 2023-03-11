from projectiles import *


class EnemyProjectile(Projectile):
    def __init__(self, spell, caster, target, groups):
        super().__init__(spell, caster, groups)
        self.speed = 9
        self.max_distance = 450
        self.direction = self.get_direction(target)
        self.animation = folder_content(f"pictures/particles/{self.spell}")
        self.image = self.animation[int(self.frame_id)]
        self.rect = self.image.get_rect(center=self.start_position)
        self.hitbox = self.rect

    def get_direction(self, player):
        projectile_vec = pygame.math.Vector2(self.start_position)
        target_vec = pygame.math.Vector2(player.hitbox.center)
        distance = (target_vec - projectile_vec).magnitude()
        if distance > 0:
            direction = (target_vec - projectile_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return direction
