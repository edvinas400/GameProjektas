import pygame.mixer

from creature import *


class Player(Creature):
    def __init__(self, position, groups, obstacles, attack, attack_delete, use_spell, spell_delete, death_particles):
        super().__init__(groups)
        self.groups = groups
        self.name = "player"
        self.death_particles = death_particles
        self.image = pygame.image.load("pictures/player2/down_still/1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-8, -31)
        self.obstacles = obstacles
        self.player_images()

        # movement
        self.status = "down"
        self.attacking = False
        self.using_spell = False

        # attack
        self.switch_cd = 400
        self.attack_cd = 400
        self.attack_time = None
        self.attack = attack
        self.attack_delete = attack_delete
        self.weapon_can_witch = True
        self.weapon_switch_time = None
        self.weapon_id = 0
        self.weapon = list(weapon_info.keys())[self.weapon_id]
        self.weapon_damage = weapon_info[self.weapon]["damage"]

        # magic
        self.spell_cd = 1000
        self.spell_time = None
        self.use_spell = use_spell
        self.spell_delete = spell_delete
        self.spell_can_switch = True
        self.spell_switch_time = None
        self.spell_id = 0
        self.spell = list(spell_info.keys())[self.spell_id]

        # stats
        self.stats = {"health": 10, "mana": 10, "attack": 10, "magic": 5, "speed": 9, "max_xp": 100}
        self.max_stats = {"health": 30, "mana": 30, "attack": 50, "magic": 30, "speed": 10, }
        self.level = 1
        self.lvlup_points = 0
        self.health = self.stats["health"] * 10
        self.mana = self.stats["mana"] * 10
        self.xp = 0
        self.speed = self.stats["speed"]
        self.vulnerable = True
        self.hurt_time = None
        self.hurt_cd = 800

        self.weapon_sound = sounds["hit"]
        self.weapon_sound.set_volume(0.1)

    def input(self):
        if not self.attacking:
            pressed = pygame.key.get_pressed()
            last_key = "]"
            if pressed[pygame.K_w]:
                last_key = "w"
            elif pressed[pygame.K_s]:
                last_key = "s"
            elif pressed[pygame.K_a]:
                last_key = "a"
            elif pressed[pygame.K_d]:
                last_key = "d"
            match last_key:
                case "w":
                    self.direction.y = -1
                    self.direction.x = 0
                    self.status = "up"
                case "s":
                    self.direction.y = 1
                    self.direction.x = 0
                    self.status = "down"
                case "a":
                    self.direction.y = 0
                    self.direction.x = -1
                    self.status = "left"
                case "d":
                    self.direction.y = 0
                    self.direction.x = 1
                    self.status = "right"
                case _:
                    self.direction.y = 0
                    self.direction.x = 0

            # attack
            if pressed[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.attack()
                self.weapon_sound.play()
            if pressed[pygame.K_q] and self.weapon_can_witch:
                self.weapon_can_witch = False
                sounds["switch"].play()
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_id += 1
                if self.weapon_id >= len(list(weapon_info.keys())):
                    self.weapon_id = 0
                self.weapon = list(weapon_info.keys())[self.weapon_id]
                self.weapon_damage = weapon_info[self.weapon]["damage"]

            # magic
            if not self.using_spell:
                if pressed[pygame.K_x] and self.mana >= spell_info[self.spell]["cost"]:
                    self.using_spell = True
                    if self.spell != "heal":
                        self.attacking = True
                        sounds[self.spell].play()
                        self.attack_time = pygame.time.get_ticks()
                    self.spell_time = pygame.time.get_ticks()
                    self.use_spell()
                if pressed[pygame.K_e] and self.spell_can_switch:
                    sounds["switch"].play()
                    self.spell_can_switch = False
                    self.spell_switch_time = pygame.time.get_ticks()
                    self.spell_id += 1
                    if self.spell_id >= len(list(spell_info.keys())):
                        self.spell_id = 0
                    self.spell = list(spell_info.keys())[self.spell_id]

    def animate(self):
        animation = self.animations[self.status]
        self.frame_id += self.frame_speed
        if self.frame_id >= len(animation):
            self.frame_id = 0
        self.image = animation[int(self.frame_id)]
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)
        self.flicker()

    def mana_regen(self):
        if self.mana < self.stats["mana"] * 10:
            self.mana += 0.001 * self.stats["magic"]
        else:
            self.mana = self.stats["mana"] * 10

    def check_lvl_up(self):
        if self.xp >= self.stats["max_xp"]:
            self.level += 1
            sounds["levelup"].play()
            self.xp -= self.stats["max_xp"]
            self.lvlup_points += 5
            self.stats["max_xp"] *= 1.6

    def status_get(self):
        # still
        if self.direction.x == 0 and self.direction.y == 0:
            if not "still" in self.status and not "attack" in self.status:
                self.status += "_still"
        # attack
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "still" in self.status:
                    self.status = self.status.replace("_still", "_attack")
                else:
                    self.status += "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def player_images(self):
        path = "pictures/player2/"
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "up_still": [], "down_still": [], "left_still": [], "right_still": [],
                           "up_attack": [], "down_attack": [], "left_attack": [], "right_attack": []}
        for animation in self.animations.keys():
            self.animations[animation] = folder_content(path + animation)

    def cooldowns(self):
        now = pygame.time.get_ticks()
        if not self.vulnerable:
            if now - self.hurt_time >= self.hurt_cd:
                self.vulnerable = True
        if self.using_spell:
            if now - self.spell_time >= self.spell_cd:
                self.using_spell = False
        if self.attacking:
            if now - self.attack_time >= self.attack_cd + weapon_info[self.weapon]["cd"]:
                self.attacking = False
                self.attack_delete()
        if not self.weapon_can_witch:
            if now - self.weapon_switch_time >= self.switch_cd:
                self.weapon_can_witch = True
        if not self.spell_can_switch:
            if now - self.spell_switch_time >= self.switch_cd:
                self.spell_can_switch = True

    def check_death(self):
        if self.health <= 0:
            self.death_particles(self.rect.center, self.name)

    def revive(self):
        self.__init__((self.hitbox.x, self.hitbox.y), self.groups, self.obstacles, self.attack, self.attack_delete, self.use_spell,
                      self.spell_delete, self.death_particles)

    def update(self):
        self.input()
        self.move(self.stats["speed"])
        self.mana_regen()
        self.cooldowns()
        self.status_get()
        self.check_death()
        self.animate()
