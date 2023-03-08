from settings import *


class HUD:
    def __init__(self):
        self.icon = pygame.image.load("pictures/player2/face2.png").convert_alpha()
        self.icon_rect = self.icon.get_rect(topleft=(20, 20))
        self.bars = pygame.image.load("pictures/bars.png").convert_alpha()
        self.bars_rect = self.bars.get_rect(topleft=(BAR_X, BAR_Y))
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        # bars
        self.hp_bar_rect = pygame.Rect(BAR_X + 23, BAR_Y + 7, BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(BAR_X + 23, BAR_Y + 40, BAR_WIDTH, BAR_HEIGHT)

    def bar(self, current, max, rect, color):
        pygame.draw.rect(self.screen, BOX_COLOR, rect)
        colored_width = current / max * rect.width
        colored_rect = rect.copy()
        colored_rect.width = colored_width
        pygame.draw.rect(self.screen, color, colored_rect)

    def player_face(self, player):
        pygame.draw.circle(self.screen, BOX_COLOR, self.icon_rect.center, 44)
        pygame.draw.circle(self.screen, BORDER_COLOR, self.icon_rect.center, 44, 6)
        self.screen.blit(self.icon, self.icon_rect)
        pygame.draw.circle(self.screen, BOX_COLOR, self.icon_rect.center + pygame.math.Vector2(-18, 35), 17)
        if player.lvlup_points > 0:
            pygame.draw.circle(self.screen, "gold", self.icon_rect.center + pygame.math.Vector2(-18, 35), 17, 5)
        else:
            pygame.draw.circle(self.screen, BORDER_COLOR, self.icon_rect.center + pygame.math.Vector2(-18, 35), 17, 5)
        text = self.font.render(str(player.level), False, FONT_COLOR)
        text_rect = text.get_rect(center=self.icon_rect.center + pygame.math.Vector2(-17, 31))
        self.screen.blit(text, text_rect)

    def selection(self, x, y, player):
        pygame.draw.circle(self.screen, BOX_COLOR, (x, y), 38)
        if not player.weapon_can_witch:
            pygame.draw.circle(self.screen, "gold", (x, y), 38, 5)
        else:
            pygame.draw.circle(self.screen, BORDER_COLOR, (x, y), 38, 5)
        pygame.draw.circle(self.screen, BOX_COLOR, (x + 60, y + 30), 38)
        if not player.spell_can_switch:
            pygame.draw.circle(self.screen, "gold", (x + 60, y + 30), 38, 5)
        else:
            pygame.draw.circle(self.screen, BORDER_COLOR, (x + 60, y + 30), 38, 5)
        weapon = pygame.image.load(weapon_info[player.weapon]["image"]).convert_alpha()
        weapon_rect = weapon.get_rect(center=(x, y))
        spell = pygame.image.load(spell_info[player.spell]["image"]).convert_alpha()
        spell_rect = spell.get_rect(center=(x + 60, y + 30))
        self.screen.blit(weapon, weapon_rect)
        self.screen.blit(spell, spell_rect)

    def display(self, player):
        self.player_face(player)
        self.bar(player.health, player.stats["health"] * 10, self.hp_bar_rect, "red")
        self.bar(player.mana, player.stats["mana"] * 10, self.mana_bar_rect, "blue")
        self.screen.blit(self.bars, self.bars_rect)
        self.selection(self.screen.get_width() * 0.035, self.screen.get_height() * 0.9, player)
