from settings import *
import copy


class Object(pygame.sprite.Sprite):
    def __init__(self, position, groups, type, image=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.image = image
        self.type = type
        if self.type in ["tiny", "2wide", "column", "normal_trees", "big_trees", "house"]:
            self.rect = self.image.get_rect(bottomleft=(position[0], position[1] + 64))
        else:
            self.rect = self.image.get_rect(topleft=position)
        self.hitbox = copy.deepcopy(self.rect)
        match self.type:
            case "up_right":
                self.hitbox.update(self.hitbox.x + 32, self.hitbox.y, 32, 32)
            case "up_left":
                self.hitbox.update(self.hitbox.x, self.hitbox.y, 32, 32)
            case "down_left":
                self.hitbox.update(self.hitbox.x, self.hitbox.y + 32, 32, 32)
            case "down_right":
                self.hitbox.update(self.hitbox.x + 32, self.hitbox.y + 32, 32, 32)
            case "full":
                self.hitbox = self.hitbox
            case "tiny":
                self.hitbox.update(self.hitbox.x + 8, self.hitbox.y + 25, 40, 32)
            case "2wide":
                self.hitbox.update(self.hitbox.x, self.hitbox.y + 64, 128, 35)
            case "column":
                self.hitbox.update(self.hitbox.x + 4, self.hitbox.y + 155, 100, 80)
            case "normal_trees":
                self.hitbox.update(self.hitbox.x + 66, self.hitbox.y + 198, 87, 40)
            case "big_trees":
                self.hitbox.update(self.hitbox.x + 82, self.hitbox.y + 245, 147, 50)
            case "house":
                self.hitbox.update(self.hitbox.x + 15, self.hitbox.y + 132, 330, 175)
