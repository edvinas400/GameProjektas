from objects import Object
from player import Player
from camera import CameraGroup
from particles import *
from hud import HUD
from enemy import Enemy
from enemy2 import Enemy2
from weapon import Weapon
from magic import Magic
from enemy_projectiles import EnemyProjectile
from levelup import LevelUp
from menu import Menu
from controls import ControlsMenu
from game_over import GameOver


class Level:
    def __init__(self, game, stage):
        self.game = game
        self.stage = stage
        self.game_paused = False
        self.menu_window = False
        self.stat_window = False
        self.controls_window = False
        self.display = pygame.display.get_surface()
        self.visible_stuff = CameraGroup(self.stage)
        self.obstacles = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.player_attackables = pygame.sprite.Group()
        self.player_attacks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_weapons = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.map(self.stage)
        self.hud = HUD()
        self.levelup = LevelUp(self.player)
        self.menu = Menu(self)
        self.controls = ControlsMenu()
        self.game_over = GameOver(self)
        self.current_attack = None
        self.current_spell = None
        self.animation_player = ParticlePlayer()
        self.magic_player = Magic(self.animation_player)

    def map(self, name):
        levels = {
            "walls": import_layout(f"csv/{name}_walls.csv"),
            "objects": import_layout(f"csv/{name}_objects.csv"),
            "creatures": import_layout(f"csv/{name}_creatures.csv"),

        }
        pictures = {
            "objects": folder_content("pictures/objects")
        }
        for type, map in levels.items():
            for yn, line in enumerate(map):
                for xn, col in enumerate(line):
                    if col != "-1":
                        x = xn * TILE_SIZE
                        y = yn * TILE_SIZE
                        if type == "creatures":
                            if col == "29":
                                self.player = Player((x, y), [self.visible_stuff], self.obstacles,
                                                     self.attack,
                                                     self.attack_delete, self.use_spell, self.spell_delete, self.death_particles)
                            elif col == "8":
                                Enemy("bigfrog", (x, y), [self.visible_stuff, self.player_attackables],
                                      self.obstacles, self.damage_player, self.death_particles,
                                      self.enemy_projectile)
                            elif col == "31":
                                Enemy("bigraccoon", (x, y), [self.visible_stuff, self.player_attackables],
                                      self.obstacles, self.damage_player, self.death_particles,
                                      self.enemy_projectile)
                            elif col == "27":
                                Enemy2("skeleton", (x, y),
                                       [self.visible_stuff, self.player_attackables, self.enemies],
                                       self.obstacles, self.enemy_attack,
                                       self.enemy_attack_delete, self.death_particles)
                            elif col == "261":
                                portal = pygame.sprite.Sprite(self.portals)
                                portal.image = pygame.Surface((64, 20))
                                portal.rect = portal.image.get_rect(topleft=(x + 10, y + 2))

                        if type == 'walls':
                            if col == "5":
                                Object((x, y), [self.obstacles], 'up_right')
                            elif col == "6":
                                Object((x, y), [self.obstacles], 'up_left')
                            elif col == "7":
                                Object((x, y), [self.obstacles], 'down_left')
                            elif col == "8":
                                Object((x, y), [self.obstacles], 'down_right')
                            else:
                                Object((x, y), [self.obstacles], 'full')

                        if type == 'objects':
                            pic = pictures["objects"][int(col)]
                            match col:
                                case "0" | "1" | "2" | "3" | "31":
                                    o_type = "tiny"
                                case "21" | "22" | "23" | "24" | "25" | "26" | "27":
                                    o_type = "2wide"
                                case "8" | "9" | "10" | "11" | "12":
                                    o_type = "column"
                                case "13" | "14" | "15" | "16" | "17" | "18" | "19" | "20":
                                    o_type = "normal_trees"
                                case "29":
                                    o_type = "big_trees"
                                case "28":
                                    o_type = "house"
                            Object((x, y), [self.visible_stuff, self.obstacles], o_type, pic)

    def player_attack_logic(self):
        if self.player_attacks:
            for attack in self.player_attacks:
                hit_sprites = pygame.sprite.spritecollide(attack, self.player_attackables, False)
                if hit_sprites:
                    for hit_sprite in hit_sprites:
                        if hit_sprite.type == "enemy":
                            hit_sprite.take_damage(self.player, attack.type)
                        else:
                            hit_sprite.kill()

    def attack(self):
        self.current_attack = Weapon(self.player, [self.visible_stuff, self.player_attacks])

    def attack_delete(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            if self.player.health <= 0:
                self.player.health = 0
            self.player.vulnerable = False
            if attack_type == "bone":
                sounds["bone"].play()
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center,
                                                   [self.visible_stuff])

    def enemy_attack(self):
        for enemy in self.enemies:
            if enemy.attacking:
                Weapon(enemy, [self.visible_stuff, self.enemy_weapons])

    def enemy_projectile(self, caster, type):
        EnemyProjectile(type, caster, self.player, [self.visible_stuff, self.enemy_projectiles])

    def enemy_attack_delete(self):
        for weapon in self.enemy_weapons:
            weapon.kill()

    def enemy_hits(self):
        if self.enemy_projectiles:
            hits = pygame.sprite.spritecollide(self.player, self.enemy_projectiles, True)
            if hits:
                for hit in hits:
                    if hit.spell == "ball":
                        sounds["frog"].play()
                        self.damage_player(enemy_info[hit.caster.name]["damage"], enemy_info[
                            hit.caster.name]["attack_type"])
                        hit.kill()
        if self.enemy_weapons:
            hits = pygame.sprite.spritecollide(self.player, self.enemy_weapons, False)
            if hits:
                for hit in hits:
                    self.damage_player(enemy_info[hit.player.name]["damage"], enemy_info[
                        hit.player.name]["attack_type"])

    def death_particles(self, position, type):
        if type == "player":
            self.player_death = self.animation_player.create_particles(type, position, [self.visible_stuff])
            sounds["gameover"].play()
            self.player.kill()
            self.game_over.update()
        else:
            self.animation_player.create_particles(type, position, [self.visible_stuff])

    def use_spell(self):
        if self.player.spell == "heal":
            self.magic_player.heal(self.player, [self.visible_stuff])
        else:
            self.magic_player.projectile(self.player, [self.visible_stuff, self.player_attacks])

    def spell_delete(self):
        if self.current_spell:
            self.current_spell.kill()
        self.current_spell = None

    def levelup_menu(self):
        if not self.menu_window and not self.controls_window:
            self.game_paused = not self.game_paused
            self.stat_window = not self.stat_window

    def escape(self):
        if self.controls_window:
            self.controls_window = False
        else:
            self.game_paused = not self.game_paused
        if not self.stat_window:
            self.menu_window = not self.menu_window

        self.stat_window = False
        self.controls_window = False

    def update(self):
        self.__init__(self.game, self.stage)

    def change_location(self):
        tps = pygame.sprite.spritecollide(self.player, self.portals, False)
        if tps:
            if self.stage == "floor_done":
                self.stage = "room"
            else:
                self.stage = "floor_done"
            stats, level, xp, lvlup_points, health, mana = [self.player.stats, self.player.level, self.player.xp,
                                                            self.player.lvlup_points, self.player.health, self.player.mana]
            self.update()
            self.game.level = self
            self.player.stats = stats
            self.player.level = level
            self.player.xp = xp
            self.player.lvlup_points = lvlup_points
            self.player.health = health
            self.player.mana = mana
            del tps

    def run(self):
        self.change_location()
        self.visible_stuff.camera_draw(self.player)
        self.hud.display(self.player)
        if self.game_paused:
            self.game.cursor_img.set_alpha(255)
            if self.stat_window:
                self.levelup.display()
            elif self.menu_window:
                self.menu.display(self)
            elif self.controls_window:
                self.controls.display()
        else:
            self.game.cursor_img.set_alpha(0)
            self.visible_stuff.update()
            self.visible_stuff.enemy_update(self.player)
            self.player_attack_logic()
            self.enemy_hits()
        if not self.player.alive() and not self.player_death.alive():
            pygame.mixer.music.stop()
            self.game_over.display(self)
