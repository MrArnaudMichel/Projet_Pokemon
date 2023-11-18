import pygame


class Tool:
    @staticmethod
    def split_image(spritesheet: pygame.Surface, x: int, y: int, witdh: int, height: int):
        return spritesheet.subsurface(pygame.Rect(x, y, witdh, height))

    @staticmethod
    def blur(background, param):
        for i in range(param):
            background = pygame.transform.smoothscale(background, (background.get_width() // 2, background.get_height() // 2))
            background = pygame.transform.smoothscale(background, (background.get_width() * 2, background.get_height() * 2))
        return background
