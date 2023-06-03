import pygame
from tiles import Tile
from set import tile_size, screen_width
from player import Player
from part import PartEffect


class Level:
    def __init__(self, level_data, surface):

        # Настройка уровня
        self.display_surface = surface
        self.setup_level(level_data)
        self.word_shift = 0
        self.current_x = 0

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def jump_part(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_part_sprite = PartEffect(pos, 'jump')
        self.dust_sprite.add(jump_part_sprite)

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
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.jump_part)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.word_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.word_shift = -8
            player.speed = 0
        else:
            self.word_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
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

        for sprite in self.tiles.sprites():
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

    def run(self):

        self.dust_sprite.update(self.word_shift)
        self.dust_sprite.draw(self.display_surface)

        self.tiles.update(self.word_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_dust()
        self.player.draw(self.display_surface)
