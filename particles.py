import copy
from settings import *


class Particles(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups, heal=False):
        super().__init__(groups)
        self.frame_id = 0
        self.frame_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_id]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = copy.deepcopy(self.rect)
        if heal:
            self.hitbox.update(self.hitbox.x, self.hitbox.y, 150, 150)

    def animate(self):
        self.frame_id += self.frame_speed
        if self.frame_id >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_id)]

    def update(self):
        self.animate()


class ParticlePlayer:
    def __init__(self):
        self.frames = {
            "aura": folder_content("pictures/particles/aura"),
            "flick": folder_content("pictures/particles/flick"),

            "bone": folder_content("pictures/particles/slash"),
            "claw": folder_content("pictures/particles/claw"),
            "ball": folder_content("pictures/particles/fire/fire"),

            "bigraccoon": folder_content("pictures/particles/smokehuge"),
            "bigfrog": folder_content("pictures/particles/smokebig"),
            "skeleton": folder_content("pictures/particles/deadbones"),
            "player": folder_content("pictures/particles/deadplayer")
        }

    def create_particles(self, type, position, groups):
        if type == "aura" or type == "flick":
            Particles(position, self.frames[type], groups, heal=True)
        elif type == "player":
            particle = Particles(position, self.frames[type], groups)
            return particle
        else:
            Particles(position, self.frames[type], groups)
