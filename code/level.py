import pygame
from supp import import_csv_layout, import_cut_graph
from set import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Case, AnimatedTile, Coin, Palm
from enemy import Enemy
from decor import Sky, Water
from player import Player
from part import PartEffect


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

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

        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

        red_layout = import_csv_layout(level_data['red'])
        self.red_sprites = self.create_tile_group(red_layout, 'red')

        self.sky = Sky(8)
        level_width = len(terr_layout[0]) * tile_size
        self.water = Water(screen_height - 360, level_width)

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

                    if type == 'enemy':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'red':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.jump_part)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('../graph/char/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)
    def enemy_reverse(self):
        for enemy in self.enemy_sprites:
            if pygame.sprite.spritecollide(enemy, self.red_sprites, False):
                enemy.reverse()

    def jump_part(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_part_sprite = PartEffect(pos, 'jump')
        self.dust_sprite.add(jump_part_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collect_sprites = self.terr_sprites.sprites() + self.case_sprites.sprites() + self.front_palms_sprites.sprites()

        for sprite in collect_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <=0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collect_sprites = self.terr_sprites.sprites() + self.case_sprites.sprites() + self.front_palms_sprites.sprites()


        for sprite in collect_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_celling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_celling and player.direction.y > 0:
            player.on_celling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_land_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprite:
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_part = PartEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_part)

    def run(self):
        self.sky.draw(self.display_surface)
        self.water.draw(self.display_surface, self.world_shift)

        self.back_palms_sprites.update(self.world_shift)
        self.back_palms_sprites.draw(self.display_surface)

        self.enemy_sprites.update(self.world_shift)
        self.red_sprites.update(self.world_shift)
        self.enemy_reverse()
        self.enemy_sprites.draw(self.display_surface)

        self.terr_sprites.update(self.world_shift)
        self.terr_sprites.draw(self.display_surface)

        self.case_sprites.update(self.world_shift)
        self.case_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        self.front_palms_sprites.update(self.world_shift)
        self.front_palms_sprites.draw(self.display_surface)

        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
