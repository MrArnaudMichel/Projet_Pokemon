import pygame


class Tool:
    @staticmethod
    def split_image(spritesheet: pygame.Surface, x: int, y: int, witdh: int, height: int):
        """
        Splits an image into a rectangular spritesheet
        :param spritesheet:
        :param x:
        :param y:
        :param witdh:
        :param height:
        :return:
        """
        return spritesheet.subsurface(pygame.Rect(x, y, witdh, height))

    @staticmethod
    def blur(background, param):
        """
        Blurs an image
        :param background:
        :param param:
        :return:
        """
        for i in range(param):
            background = pygame.transform.smoothscale(background,
                                                      (background.get_width() // 2, background.get_height() // 2))
            background = pygame.transform.smoothscale(background,
                                                      (background.get_width() * 2, background.get_height() * 2))
        return background

    @staticmethod
    def create_text(text: str, size: int, color: tuple[int, int, int], font: str = "Roboto-Light", bold: bool = False):
        """
        Creates a text surface
        :param text:
        :param size:
        :param color:
        :param font:
        :param bold:
        :return:
        """
        font = pygame.font.Font(f"../../assets/fonts/{font}.ttf", size)
        if bold:
            font.set_bold(True)
        return font.render(text, True, color)

    @staticmethod
    def add_text_to_surface(surface: pygame.surface.Surface, text: pygame.surface.Surface, x: int, y: int):
        """
        Adds a text to the surface with the given x and y coordinates
        :param surface:
        :param text:
        :param x:
        :param y:
        :return:
        """
        surface.blit(text, (x, y))