import pygame
import pytmx
import pyscroll

from screen import Screen


class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None

        self.switch_map("map0")

    def switch_map(self, map: str):
        self.tmx_data = pytmx.load_pygame(f"../../assets/map/{map}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

    def update(self):
        self.group.draw(self.screen.get_display())
