import pygame


class Switch:
    def __init__(self, type: str, name: str, hitbox: pygame.Rect, port: int):
        self.type = type
        self.name = name
        self.hitbox = hitbox
        self.port = port

    def check_collision(self, temp_hitbox):
        return self.hitbox.colliderect(temp_hitbox)
