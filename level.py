import pygame
from tiles import Tile
from set import tile_size
from player import Player

class Level:
    def __init__(self, level_data, surface):

        # Настройка уровня
        self.display_surface = surface
        self.setup_level(level_data)
        self.word_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    player_sprite = Player((x,y))
                    self.tiles.add(player_sprite)

    def run(self):
        self.tiles.update(self.word_shift)
        self.tiles.draw(self.display_surface)

        self.player.draw(self.display_surface)
