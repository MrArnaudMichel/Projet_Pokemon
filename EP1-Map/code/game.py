import pygame

from screen import Screen
from map import Map

class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)

    def run(self):
        while self.running:
            self.map.update()
            self.screen.update()
