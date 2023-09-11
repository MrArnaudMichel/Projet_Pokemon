import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.pokedollars: int = 0

    def update(self) -> None:
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            if self.keylistener.key_pressed(pygame.K_q):
                self.move_left()
            elif self.keylistener.key_pressed(pygame.K_d):
                self.move_right()
            elif self.keylistener.key_pressed(pygame.K_z):
                self.move_up()
            elif self.keylistener.key_pressed(pygame.K_s):
                self.move_down()
