import pygame

from tool import Tool
from keylistener import KeyListener

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener):
        super().__init__()
        self.keylistener = keylistener
        self.spritesheet = pygame.image.load("../../assets/sprite/hero_01_red_m_walk.png")
        self.image = Tool.split_image(self.spritesheet, 0, 0, 24, 32)
        self.position = [0, 0]
        self.rect: pygame.Rect = pygame.Rect(0, 0, 16, 32)
        self.all_images = self.get_all_images()
        self.index_image = 0

    def update(self):
        self.check_move()
        self.rect.topleft = self.position

    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_q):
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_d):
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_z):
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_s):
            self.move_down()

    def move_left(self):
        self.position[0] -= 1
        self.image = self.all_images["left"][self.index_image]

    def move_right(self):
        self.position[0] += 1
        self.image = self.all_images["right"][self.index_image]

    def move_up(self):
        self.position[1] -= 1
        self.image = self.all_images["up"][self.index_image]

    def move_down(self):
        self.position[1] += 1
        self.image = self.all_images["down"][self.index_image]

    def get_all_images(self):
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }
        for i in range(4):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(self.spritesheet, i * 24, j*32, 24, 32))
        return all_images
