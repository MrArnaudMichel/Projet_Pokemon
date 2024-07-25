import pygame


class Screen:
    def __init__(self) -> None:
        self.imagescreen: pygame.Surface = pygame.display.get_surface()
        self.display: pygame.display = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Pokémon")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.framerate: int = 240
        self.deltatime: float = 0.0

    def update(self) -> None:
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.framerate)
        self.imagescreen = self.display.copy()
        self.display.fill((0, 0, 0))
        self.deltatime = self.clock.get_time()

    def get_delta_time(self) -> float:
        return self.deltatime

    def get_size(self) -> tuple[int, int]:
        return self.display.get_size()

    def get_display(self) -> pygame.display:
        return self.display

    def image_screen(self):
        return self.imagescreen
