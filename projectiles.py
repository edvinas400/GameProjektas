from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, spell, caster, groups):
        super().__init__(groups)
        self.frame_id = 0
        self.frame_speed = 0.25
        self.speed = 7
        self.max_distance = 225
        self.start_position = caster.rect.center
        self.spell = spell
        self.caster = caster
        self.type = "projectile"

    def move(self):
        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center

    def disappear(self):
        distance = self.get_distance()
        if distance > self.max_distance:
            self.kill()

    def animate(self):
        self.frame_id += self.frame_speed
        if self.frame_id >= len(self.animation):
            self.frame_id = 0
        self.image = self.animation[int(self.frame_id)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def get_distance(self):
        projectile_vec = pygame.math.Vector2(self.rect.center)
        caster_vec = pygame.math.Vector2(self.start_position)
        distance = (caster_vec - projectile_vec).magnitude()
        return distance

    def update(self):
        self.move()
        self.disappear()
        self.animate()
