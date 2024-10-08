import pygame


class Tool:
    @staticmethod
    def split_image(spritesheet: pygame.Surface, x: int, y: int, witdh: int, height: int):
        return spritesheet.subsurface(pygame.Rect(x, y, witdh, height))

    @staticmethod
    def blur(background, param):
        for i in range(param):
            background = pygame.transform.smoothscale(background,
                                                      (background.get_width() // 2, background.get_height() // 2))
            background = pygame.transform.smoothscale(background,
                                                      (background.get_width() * 2, background.get_height() * 2))
        return background

    @staticmethod
    def create_text(text: str, size: int, color: tuple[int, int, int], font: str = "Roboto-Light", bold: bool = False):
        font = pygame.font.Font(f"../../assets/fonts/{font}.ttf", size)
        if bold:
            font.set_bold(True)
        return font.render(text, True, color)

    @staticmethod
    def add_text_to_surface(surface, text, x, y):
        surface.blit(text, (x, y))