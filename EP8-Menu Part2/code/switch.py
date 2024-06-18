import pygame


class Switch:
    def __init__(self, type: str, name: str, hitbox: pygame.Rect, port: int):
        self.type: str = type
        self.name: str = name
        self.hitbox: pygame.Rect = hitbox
        self.port: port = port

    def check_collision(self, temp_hitbox) -> bool:
        return self.hitbox.colliderect(temp_hitbox)
