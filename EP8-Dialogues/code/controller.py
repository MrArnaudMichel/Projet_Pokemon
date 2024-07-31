import pygame


class Controller:
    """
    Controller class to manage the keys
    """
    def __init__(self):
        """
        Initialize the keys dictionary
        """
        self.keys: dict[str: int] = {
            "up": pygame.K_z,
            "down": pygame.K_s,
            "left": pygame.K_q,
            "right": pygame.K_d,
            "action": pygame.K_e,
            "bike": pygame.K_b,
            "quit": pygame.K_ESCAPE,
        }

    def get_key(self, key: str) -> int:
        """
        Get the key value from the key name
        :param key:
        :return:
        """
        return self.keys[key]

    def add_key(self, key: str, value: int) -> None:
        """
        Add a key to the keys dictionary
        :param key:
        :param value:
        :return:
        """
        self.keys[key] = value
