import pygame
from supp import import_csv_layout, import_cut_graph
from set import tile_size
from tiles import Tile, StaticTile, Case, AnimatedTile, Coin, Palm

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = -5

        terr_layout = import_csv_layout(level_data['terr'])
        self.terr_sprites = self.create_tile_group(terr_layout, 'terr')

        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        case_layout = import_csv_layout(level_data['case'])
        self.case_sprites = self.create_tile_group(case_layout, 'case')

        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        front_palms_layout = import_csv_layout(level_data['front palms'])
        self.front_palms_sprites = self.create_tile_group(front_palms_layout, 'front palms')

        back_palms_layout = import_csv_layout(level_data['back palms'])
        self.back_palms_sprites = self.create_tile_group(back_palms_layout, 'back palms')
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terr':
                        terr_tale_list = import_cut_graph('../graph/terr/sheet.png')
                        tile_surface = terr_tale_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graph('../graph/decor/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'case':
                        sprite = Case(tile_size, x, y)

                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size, x, y, '../graph/coins/gold')
                        if val == '1': sprite = Coin(tile_size, x, y, '../graph/coins/silver')

                    if type == 'front palms':
                        if val == '2': sprite = Palm(tile_size, x, y, '../graph/terr/palm_small', 38)
                        if val == '1': sprite = Palm(tile_size, x, y, '../graph/terr/palm_large', 64)

                    if type == 'back palms':
                        sprite = Palm(tile_size, x, y, '../graph/terr/palm_bg', 64)

                    sprite_group.add(sprite)
        return sprite_group
    def run(self):
        self.terr_sprites.update(self.world_shift)
        self.terr_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        self.case_sprites.update(self.world_shift)
        self.case_sprites.draw(self.display_surface)

        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        self.front_palms_sprites.update(self.world_shift)
        self.front_palms_sprites.draw(self.display_surface)

        self.back_palms_sprites.update(self.world_shift)
        self.back_palms_sprites.draw(self.display_surface)