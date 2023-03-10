from enemy import *


class Enemy3(Enemy):
    def __init__(self, name, position, groups, obstacles, damage_player, death_particles, enemy_projectile):
        super().__init__(name, position, groups, obstacles, damage_player, death_particles, enemy_projectile)
        self.hitbox = copy.deepcopy(self.rect)
        self.hitbox.update(self.hitbox.x, self.hitbox.y, 24, 2)

    def status_get(self, player):
        distance = self.distance_direction_get(player)[0]
        direction = self.distance_direction_get(player)[1]
        if not self.attacking:
            if distance <= self.stats["attack_radius"] and self.can_attack:
                if direction.x > 0:
                    self.status = "right_attack"
                else:
                    self.status = "left_attack"
                self.attacking = True
                self.frame_id = 0
            elif self.stats["attack_radius"] <= distance <= self.stats["vision_radius"]:
                if direction.x > 0:
                    self.status = "right_move"
                else:
                    self.status = "left_move"
            else:
                if direction.x > 0:
                    self.status = "right_still"
                else:
                    self.status = "left_still"

    def enemy_images(self, name):
        self.animations = {"still": [], "left_still": [], "left_move": [], "left_attack": [], "right_still": [], "right_move": [],
                           "right_attack": []}
        path = f"pictures/enemies/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = folder_content(path + animation)

    def actions(self, player):
        if "attack" in self.status:
            self.attack_time = pygame.time.get_ticks()
            self.direction = pygame.Vector2()
        elif "move" in self.status:
            self.direction = self.distance_direction_get(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_id += self.frame_speed
        if "attack" in self.status and round(self.frame_id) == len(animation) / 2:
            self.damage_player(self.stats["damage"], self.stats["attack_type"])
        if self.frame_id >= len(animation):
            if "attack" in self.status:
                self.attacking = False
                self.can_attack = False
            self.frame_id = 0
        self.image = animation[int(self.frame_id)]
        self.rect = self.image.get_rect(center=self.hitbox.center + pygame.math.Vector2(0, -20))
        self.flicker()
