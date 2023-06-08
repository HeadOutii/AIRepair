import pygame
from supp import import_csv_layout

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface

        terr_layout = import_csv_layout(level_data['terr'])
    def run(self):
        pass
