from creature import *
import copy


class Enemy(Creature):
    def __init__(self, name, position, groups, obstacles, damage_player, death_particles, enemy_projectile):
        super().__init__(groups)
        self.type = "enemy"
        self.enemy_images(name)
        self.status = "still"
        self.image = self.animations[self.status][self.frame_id]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = copy.deepcopy(self.rect)
        self.hitbox.update(self.hitbox.x, self.hitbox.y, 140, 60)
        self.obstacles = obstacles

        # stats
        self.name = name
        self.stats = enemy_info[name]
        self.hp = self.stats["health"]

        # interaction
        self.attacking = False
        self.can_attack = True
        self.attack_cd = 1000
        self.attack_time = None
        self.damage_player = damage_player
        self.projectile = enemy_projectile
        self.death_particles = death_particles
        self.vulnerable = True
        self.hurt_time = None
        self.hurt_cd = 800

    def distance_direction_get(self, player):
        enemy_vec = pygame.math.Vector2(self.hitbox.center)
        player_vec = pygame.math.Vector2(player.hitbox.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        if not player.alive():
            distance = 1000
        return distance, direction

    def status_get(self, player):
        distance = self.distance_direction_get(player)[0]
        if not self.attacking:
            if distance <= self.stats["attack_radius"] and self.can_attack:
                self.status = "attack"
                self.attacking = True
                if self.name == "bigraccoon":
                    sounds["slash"].play()
                self.frame_id = 0
            elif self.stats["attack_radius"] <= distance <= self.stats["vision_radius"]:
                self.status = "move"
            else:
                self.status = "still"

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.direction = pygame.Vector2()
        elif self.status == "move":
            self.direction = self.distance_direction_get(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def cooldown(self):
        now = pygame.time.get_ticks()
        if not self.can_attack:
            if now - self.attack_time >= self.attack_cd:
                self.can_attack = True
        if not self.vulnerable:
            if now - self.hurt_time >= self.hurt_cd:
                self.vulnerable = True

    def enemy_images(self, name):
        self.animations = {"still": [], "move": [], "attack": []}
        path = f"pictures/enemies/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = folder_content(path + animation)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_id += self.frame_speed
        if self.name == "bigraccoon" and self.status == "attack" and round(self.frame_id) == len(
                animation) / 2:
            self.damage_player(self.stats["damage"], self.stats["attack_type"])
        if self.frame_id >= len(animation):
            if self.status == "attack":
                if self.name == "bigfrog":
                    self.projectile(self, self.stats["attack_type"])
                self.can_attack = False
                self.attacking = False
            self.frame_id = 0
        self.image = animation[int(self.frame_id)]
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)
        self.flicker()

    def update(self):
        self.move(self.stats["speed"])
        self.cooldown()
        self.animate()

    def enemy_update(self, player):
        self.status_get(player)
        self.actions(player)
        self.see_if_dead(player)
