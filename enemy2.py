from creature import *
from weapon import *
import copy


class Enemy2(Creature):
    def __init__(self, name, position, groups, obstacles, attack, attack_delete, death_particles):
        super().__init__(groups)
        self.type = "enemy"
        self.enemy_images(name)
        self.status = "down"
        self.image = self.animations[self.status][self.frame_id]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = copy.deepcopy(self.rect)
        self.hitbox.update(self.hitbox.x, self.hitbox.y + 30, 50, 30)
        self.obstacles = obstacles

        # stats
        self.name = name
        self.weapon = enemy_info[name]["attack_type"]
        self.stats = enemy_info[name]
        self.hp = self.stats["health"]

        # interaction
        self.death_particles = death_particles
        self.attacking = False
        self.state = "still"
        self.attack = attack
        self.attack_delete = attack_delete
        self.can_attack = True
        self.attack_cd = 2000
        self.attack_time = None
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
            if distance <= self.stats["attack_radius"]:
                self.state = "attack"
            elif self.stats["vision_radius"] >= distance >= self.stats["attack_radius"]:
                self.state = "move"
            else:
                self.state = "still"

    def actions(self, player):
        direction = self.distance_direction_get(player)[1]
        if self.state != "still" and not self.attacking:
            if direction.x > 0 and abs(direction.x) > abs(direction.y):
                self.status = "right"
            if direction.x < 0 and abs(direction.x) > abs(direction.y):
                self.status = "left"
            if direction.y > 0 and abs(direction.x) < abs(direction.y):
                self.status = "down"
            if direction.y < 0 and abs(direction.x) < abs(direction.y):
                self.status = "up"
        if self.state == "attack":
            self.direction = pygame.Vector2()
            if self.can_attack:
                self.attacking = True
                self.attack()
                if "attack" not in self.status:
                    self.attack_time = pygame.time.get_ticks()
                    if "still" in self.status:
                        self.status = self.status.replace("_still", "_attack")
                    else:
                        self.status += "_attack"
            else:
                if "attack" in self.status:
                    self.status = self.status.replace("_attack", "_still")
                else:
                    if "still" not in self.status:
                        self.status += "_still"
        elif self.state == "move":
            self.direction = self.distance_direction_get(player)[1]
        else:
            self.direction = pygame.math.Vector2()
            if "still" not in self.status:
                self.status += "_still"

    def cooldown(self):
        now = pygame.time.get_ticks()
        if not self.can_attack:
            if now - self.attack_time >= self.attack_cd:
                self.can_attack = True
        if not self.vulnerable:
            if now - self.hurt_time >= self.hurt_cd:
                self.vulnerable = True

    def enemy_images(self, name):
        path = f"pictures/enemies/{name}/"
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "up_still": [], "down_still": [], "left_still": [], "right_still": [],
                           "up_attack": [], "down_attack": [], "left_attack": [], "right_attack": []}
        for animation in self.animations.keys():
            self.animations[animation] = folder_content(path + animation)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_id += self.frame_speed
        if self.frame_id >= len(animation):
            if "attack" in self.status:
                self.attacking = False
                self.status = self.status.replace("_attack", "")
                self.can_attack = False
                self.attack_delete()
            self.frame_id = 0
        self.image = animation[int(self.frame_id)]
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)
        self.flicker()

    def see_if_dead(self, player):
        if self.hp <= 0:
            self.death_particles(self.rect.center, self.name)
            player.xp += self.stats["xp"]
            player.check_lvl_up()
            self.kill()
            sounds[self.name].play()
            self.attack_delete()

    def update(self):
        self.move(self.stats["speed"])
        self.cooldown()
        self.animate()

    def enemy_update(self, player):
        self.see_if_dead(player)
        self.status_get(player)
        self.actions(player)
