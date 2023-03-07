from player_projectiles import *
from settings import *


class Magic:
    def __init__(self, player):
        self.particle_player = player

    def heal(self, player, groups):
        if player.mana >= spell_info[player.spell]["cost"]:
            sounds["heal"].set_volume(0.1)
            sounds["heal"].play()
            player.health += spell_info[player.spell]["power"] + player.stats["magic"]
            player.mana -= spell_info[player.spell]["cost"]
            if player.health > player.stats["health"] * 10:
                player.health = player.stats["health"] * 10
            self.particle_player.create_particles("aura", player.rect.center + pygame.math.Vector2(0, 15),
                                                  groups)
            self.particle_player.create_particles("flick", player.rect.center - pygame.math.Vector2(0, 20),
                                                  groups)

    def projectile(self, player, groups):
        if player.mana >= spell_info[player.spell]["cost"]:
            PlayerProjectile(player.spell, player, groups)
            player.mana -= spell_info[player.spell]["cost"]
