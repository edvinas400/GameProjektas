from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.halfw = WIDTH // 2
        self.halfh = HEIGHT // 2
        self.off = pygame.math.Vector2()
        self.floor_image = pygame.image.load("pictures/maps/bigmapasfinal.png").convert()
        self.floor_rect = self.floor_image.get_rect(topleft=(0, 0))

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, "type") and sprite.type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def object_sort(self, object):
        try:
            if object.type == "projectile":
                return object.hitbox.centery + 130
            else:
                return object.hitbox.centery
        except:
            return object.hitbox.centery

    def camera_draw(self, player):
        self.off.x = player.rect.centerx - self.halfw
        self.off.y = player.rect.centery - self.halfh
        floor_position = self.floor_rect.topleft - self.off
        self.display.blit(self.floor_image, floor_position)

        for object in sorted(self.sprites(), key=self.object_sort):
            new_position = object.rect.topleft - self.off
            self.display.blit(object.image, new_position)
