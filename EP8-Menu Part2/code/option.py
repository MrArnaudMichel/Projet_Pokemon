import json
import pygame
import datetime

from controller import Controller
from map import Map
from player import Player
from screen import Screen
from sql import SQL
from save import Save
from tool import Tool
from keylistener import KeyListener


class Option:
    def __init__(self, screen: Screen, controller: Controller, map: Map, language: str, save: Save,
                 keylistener: KeyListener):
        self.screen: Screen = screen
        self.controller: Controller = controller
        self.map: Map = map
        self.language: str = language
        self.save: Save = save
        self.sql: SQL = SQL()
        self.player: Player = self.map.player
        self.keylistener = keylistener

        self.full_background: pygame.Surface = pygame.surface.Surface(self.screen.get_size())
        self.image_background: pygame.Surface | None = None
        self.initialization: bool = False

        self.background_color = (4, 18, 18)
        self.background: pygame.Surface = pygame.surface.Surface((self.screen.get_size()[0], 80))
        self.background.fill(self.background_color)

    def update(self):
        if not self.initialization:
            self.initialization = True
            self.initialize()
        self.draw()
        self.check_end()

    def initialize(self):
        self.image_background = self.screen.image_screen()
        self.image_background = Tool.blur(self.image_background, 2)

    def draw(self):
        self.player.update_ingame_time()
        self.full_background.blit(self.image_background, (0, 0))
        self.full_background.blit(self.background, (0, 0))
        self.full_background.blit(self.background, (0, self.screen.get_size()[1] - self.background.get_height()))

        self.screen.get_display().blit(self.full_background, (0, 0))

    def check_end(self):
        if self.keylistener.key_pressed(self.controller.get_key("quit")):
            self.initialization = False
            self.player.menu_option = False
            self.keylistener.remove_key(self.controller.get_key("quit"))
            return
