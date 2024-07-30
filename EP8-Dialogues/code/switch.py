import pygame


class Switch:
    """
    Switch class to manage the switch in the map
    """
    def __init__(self, type: str, name: str, hitbox: pygame.Rect, port: int):
        """
        Initialize the switch
        :param type:
        :param name:
        :param hitbox:
        :param port:
        """
        self.type: str = type
        self.name: str = name
        self.hitbox: pygame.Rect = hitbox
        self.port: port = port

    def check_collision(self, temp_hitbox) -> bool:
        """
        Check the collision with the switch
        :param temp_hitbox:
        :return:
        """
        return self.hitbox.colliderect(temp_hitbox)
