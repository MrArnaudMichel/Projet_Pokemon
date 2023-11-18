import pygame

class Controller:
    def __init__(self):
        self.keys = {
            "up": pygame.K_z,
            "down": pygame.K_s,
            "left": pygame.K_q,
            "right": pygame.K_d,
            "action": pygame.K_e,
            "bike": pygame.K_b,
            "quit": pygame.K_ESCAPE,
        }

    def get_key(self, key: str):
        return self.keys[key]

    def add_key(self, key: str, value: int):
        self.keys[key] = value