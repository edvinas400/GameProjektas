from csv import reader
from os import walk
import pygame
import pickle
import math

pygame.mixer.init()

WIDTH = 1500
HEIGHT = 800
FPS = 60
TILE_SIZE = 64

# hud
BAR_HEIGHT = 15
BAR_X = 100
BAR_Y = 30
BAR_WIDTH = 171
BOX_COLOR = "grey"
BORDER_COLOR = "black"
BOX_SIZE = 80
FONT = "other/normal.ttf"
BIG_FONT = "other/gameboy.ttf"
FONT_SIZE = 20
FONT_COLOR = "black"

weapon_info = {
    "sai": {"cd": 150, "damage": 35, "image": "pictures/weapons/sai/full.png"},
    "lance": {"cd": 400, "damage": 65, "image": "pictures/weapons/lance/full.png"},
    "sword": {"cd": 300, "damage": 60, "image": "pictures/weapons/sword/full.png"},
    "stick": {"cd": 200, "damage": 25, "image": "pictures/weapons/stick/full.png"}
}

spell_info = {
    "thunder": {"cost": 0, "power": 30, "image": "pictures/particles/ScrollThunder.png"},
    "leaf": {"cost": 10, "power": 30, "image": "pictures/particles/ScrollPlant.png"},
    "ice": {"cost": 10, "power": 30, "image": "pictures/particles/ScrollIce.png"},
    "fireball": {"cost": 10, "power": 30, "image": "pictures/particles/ScrollFire.png"},
    "heal": {"cost": 25, "power": 20, "image": "pictures/particles/ScrollHeal.png"}
}

enemy_info = {
    "bigraccoon": {"health": 600, "xp": 60, "damage": 40, "speed": 3, "attack_radius": 80,
                   "vision_radius": 290, "attack_type": "claw"},
    "bigfrog": {"health": 400, "xp": 50, "damage": 30, "speed": 3, "attack_radius": 300,
                "vision_radius": 350, "attack_type": "ball", },
    "skeleton": {"health": 250, "xp": 40, "damage": 20, "speed": 3, "attack_radius": 70,
                 "vision_radius": 250, "attack_type": "bone", },
    "knight": {"health": 1400, "xp": 110, "damage": 70, "speed": 3, "attack_radius": 70,
               "vision_radius": 290, "attack_type": "swordy", },
    "santa": {"health": 300, "xp": 50, "damage": 30, "speed": 3, "attack_radius": 60,
              "vision_radius": 210, "attack_type": "punch", },
    "frog": {"health": 250, "xp": 50, "damage": 40, "speed": 3, "attack_radius": 70,
             "vision_radius": 200, "attack_type": "swordy", }
}

sounds = {
    "hit": pygame.mixer.Sound("sounds/hit.wav"),
    "slash": pygame.mixer.Sound("sounds/slash.wav"),
    "bigfrog": pygame.mixer.Sound("sounds/frog.wav"),
    "bone": pygame.mixer.Sound("sounds/bone.wav"),
    "swordy": pygame.mixer.Sound("sounds/sword.wav"),
    "thunder": pygame.mixer.Sound("sounds/thunder.wav"),
    "leaf": pygame.mixer.Sound("sounds/leaf.wav"),
    "ice": pygame.mixer.Sound("sounds/ice.wav"),
    "fireball": pygame.mixer.Sound("sounds/fireball.wav"),
    "heal": pygame.mixer.Sound("sounds/heal.wav"),
    "click": pygame.mixer.Sound("sounds/click2.wav"),
    "levelup": pygame.mixer.Sound("sounds/levelup.wav"),
    "gameover": pygame.mixer.Sound("sounds/gameover.wav"),
    "switch": pygame.mixer.Sound("sounds/swap.wav"),
    "poof": pygame.mixer.Sound("sounds/poof.wav"),
    "skeleton": pygame.mixer.Sound("sounds/skeleton.wav"),
    "knight": pygame.mixer.Sound("sounds/thud.wav"),
    "frog": pygame.mixer.Sound("sounds/croak.wav"),
    "punch": pygame.mixer.Sound("sounds/punch.wav"),

}

exit_coordinates = {
    "room": (2000, 4730),
    "cave": (3270, 6480)
}

for sound in sounds:
    sounds[sound].set_volume(0.2)
sounds["switch"].set_volume(0.1)
sounds["bigfrog"].set_volume(0.05)
sounds["frog"].set_volume(0.4)
sounds["skeleton"].set_volume(0.05)


def import_layout(path):
    map = []
    with open(path) as layout:
        layout = reader(layout)
        for line in layout:
            map.append(list(line))
        return map


def folder_content(path):
    images = []
    for a, b, imgs in walk(path):
        for img in imgs:
            full_path = path + "/" + img
            image = pygame.image.load(full_path).convert_alpha()
            images.append(image)
    return images


def save(level):
    with open('saves/save.pkl', 'wb') as outp:
        save = [level.player.hitbox, level.player.stats, level.player.level, level.player.xp,
                level.player.lvlup_points, level.player.health, level.player.mana, level.stage]
        pickle.dump(save, outp, pickle.HIGHEST_PROTOCOL)


def load(game):
    with open('saves/save.pkl', 'rb') as inp:
        hitbox, stats, level, xp, lvlup_points, health, mana, stage = pickle.load(inp)
        game.player.hitbox = hitbox
        game.player.stats = stats
        game.player.level = level
        game.player.xp = xp
        game.player.lvlup_points = lvlup_points
        game.player.health = health
        game.player.mana = mana
        game.stage = stage
        return stage


def float(amplitude, freq):
    value = math.sin(pygame.time.get_ticks() / freq)
    return amplitude * value


def town_music():
    pygame.mixer.music.load("music/town.wav")
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)


def menu_music():
    pygame.mixer.music.load("music/theme.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
