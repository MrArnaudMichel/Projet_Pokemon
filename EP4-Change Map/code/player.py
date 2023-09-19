import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.pokedollars: int = 0

        self.switchs: list[Switch] | None = None
        self.change_map: Switch | None = None

    def update(self) -> None:
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                temp_hitbox.x -= 16
                self.check_collisions_switchs(temp_hitbox)
                self.move_left()
            elif self.keylistener.key_pressed(pygame.K_d):
                temp_hitbox.x += 16
                self.check_collisions_switchs(temp_hitbox)
                self.move_right()
            elif self.keylistener.key_pressed(pygame.K_z):
                temp_hitbox.y -= 16
                self.check_collisions_switchs(temp_hitbox)
                self.move_up()
            elif self.keylistener.key_pressed(pygame.K_s):
                temp_hitbox.y += 16
                self.check_collisions_switchs(temp_hitbox)
                self.move_down()

    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
        return None
