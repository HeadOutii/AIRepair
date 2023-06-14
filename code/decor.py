import pygame
from set import vert_tile_number, tile_size, screen_width
from tiles import AnimatedTile

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('../graph/decor/sky/top.png').convert()
        self.middle = pygame.image.load('../graph/decor/sky/middle.png').convert()
        self.bottom = pygame.image.load('../graph/decor/sky/bottom.png').convert()
        self.horizon = horizon

        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vert_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 545
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(200, x, y, '../graph/decor/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)