import pygame

from screen import Screen
from map import Map
from entity import Entity
from keylistener import KeyListener


class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = KeyListener()
        self.entity = Entity(self.keylistener)
        self.map.add_player(self.entity)

    def run(self):
        while self.running:
            self.handle_input()
            self.map.update()
            self.screen.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)

