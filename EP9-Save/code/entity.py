import pygame

from screen import Screen
from tool import Tool


class Entity(pygame.sprite.Sprite):
    """
    Entity class to manage the entities
    """
    def __init__(self, screen: Screen, x: int, y: int):
        """
        Initialize the entity
        :param screen:
        :param x:
        :param y:
        """
        super().__init__()
        self.screen: Screen = screen
        self.spritesheet: pygame.image = pygame.image.load("../../assets/sprite/hero_01_red_m_walk.png")
        self.image: pygame.image = Tool.split_image(self.spritesheet, 0, 0, 24, 32)
        self.position: pygame.math.Vector2 = pygame.math.Vector2(x, y)
        self.rect: pygame.Rect = self.image.get_rect()
        self.all_images: dict[str, list[pygame.image]] = self.get_all_images(self.spritesheet)
        self.index_image: int = 0
        self.image_part: int = 0
        self.reset_animation: bool = False
        self.hitbox: pygame.Rect = pygame.Rect(0, 0, 16, 16)

        self.step: int = 0
        self.animation_walk: bool = False
        self.direction: str = "down"

        self.animtion_step_time: float = 0.0
        self.action_animation: int = 16

        self.speed: int = 1

    def update(self) -> None:
        """
        Update the entity
        :return:
        """
        self.animation_sprite()
        self.move()
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        self.image = self.all_images[self.direction][self.index_image]

    def move_left(self) -> None:
        """
        Move the entity to the left
        :return:
        """
        self.animation_walk = True
        self.direction = "left"

    def move_right(self) -> None:
        """
        Move the entity to the right
        :return:
        """
        self.animation_walk = True
        self.direction = "right"

    def move_up(self) -> None:
        """
        Move the entity to the up
        :return:
        """
        self.animation_walk = True
        self.direction = "up"

    def move_down(self) -> None:
        """
        Move the entity to the down
        :return:
        """
        self.animation_walk = True
        self.direction = "down"

    def animation_sprite(self) -> None:
        """
        Animate the sprite
        :return:
        """
        if int(self.step // 8) + self.image_part >= 4:
            self.image_part = 0
            self.reset_animation = True
        self.index_image = int(self.step // 8) + self.image_part

    def move(self) -> None:
        """
        Move the entity on the screen
        :return:
        """
        if self.animation_walk:
            self.animtion_step_time += self.screen.get_delta_time()
            if self.step < 16 and self.animtion_step_time >= self.action_animation:
                self.step += self.speed
                if self.direction == "left":
                    self.position.x -= self.speed
                elif self.direction == "right":
                    self.position.x += self.speed
                elif self.direction == "up":
                    self.position.y -= self.speed
                elif self.direction == "down":
                    self.position.y += self.speed
                self.animtion_step_time = 0
            elif self.step >= 16:
                self.step = 0
                self.animation_walk = False
                if self.reset_animation:
                    self.reset_animation = False
                else:
                    if self.image_part == 0:
                        self.image_part = 2
                    else:
                        self.image_part = 0

    def align_hitbox(self) -> None:
        """
        Align the hitbox with map grid (16x16)
        :return:
        """
        self.position.x += 16
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.x % 16 != 0:
            self.rect.x -= 1
            self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.y % 16 != 0:
            self.rect.y -= 1
            self.hitbox.midbottom = self.rect.midbottom
        self.position = pygame.math.Vector2(self.rect.center)

    def get_all_images(self, spritesheet: pygame.image) -> dict[str, list[pygame.image]]:
        """
        Get all images from the spritesheet
        :param spritesheet:
        :return:
        """
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }

        width: int = spritesheet.get_width() // 4
        height: int = spritesheet.get_height() // 4

        for i in range(4):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(spritesheet, i * width, j * height, 24, 32))
        return all_images
