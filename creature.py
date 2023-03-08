from settings import *


class Creature(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_id = 0
        self.frame_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        self.hitbox.x += self.direction.x * speed
        self.collision('x')
        self.hitbox.y += self.direction.y * speed
        self.collision('y')
        self.rect.midbottom = self.hitbox.midbottom

    def flicker(self):
        if not self.vulnerable:
            value = math.sin(pygame.time.get_ticks())
            if value >= 0:
                alpha = 255
            else:
                alpha = 0
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def collision(self, axis):
        if axis == "x":
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = obstacle.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = obstacle.hitbox.right
        if axis == "y":
            for obstacle in self.obstacles:
                if obstacle.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = obstacle.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = obstacle.hitbox.bottom

    def take_damage(self, player, attack_type):
        if self.vulnerable:
            if attack_type == "weapon":
                self.hp -= player.stats["attack"] + weapon_info[player.weapon]["damage"]
            else:
                self.hp -= player.stats["magic"] + spell_info[player.spell]["power"]
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()

    def see_if_dead(self, player):
        if self.hp <= 0:
            self.death_particles(self.rect.center, self.name)
            player.xp += self.stats["xp"]
            player.check_lvl_up()
            self.kill()
            if self.name in ("bigraccoon", "bigfrog"):
                sounds["poof"].play()
