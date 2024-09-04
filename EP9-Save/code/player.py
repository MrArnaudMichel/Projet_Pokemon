import datetime

import pygame

from controller import Controller
from entity import Entity
from keylistener import KeyListener
from pokemon import Pokemon
from screen import Screen
from switch import Switch


class Player(Entity):
    """
    Player class to manage the player
    """
    def __init__(self, screen: Screen, controller: Controller, x: int, y: int, keylistener: KeyListener,
                 ingame_time: datetime.timedelta = datetime.timedelta(seconds=0), gender: str = "red_m") -> None:
        """
        Initialize the player
        :param screen:
        :param controller:
        :param x:
        :param y:
        :param keylistener:
        :param ingame_time:
        """
        super().__init__(screen, x, y, f"hero_01_{gender}")
        self.keylistener: KeyListener = keylistener
        self.controller: Controller = controller
        self.pokemons: list[Pokemon] = []
        self.inventory: None = None
        self.pokedex: None = None

        self.name: str = "Lucas"
        self.gender: str = gender
        self.pokedollars: int = 0

        self.pokemons.append(Pokemon.create_pokemon("Bulbasaur", 5))
        self.ingame_time: datetime.timedelta = ingame_time

        self.can_move = True

        self.spritesheet_bike: pygame.image = pygame.image.load("../../assets/sprite/hero_01_red_m_cycle_roll.png")

        self.menu_option: bool = False

        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None

    def from_dict(self, data: dict) -> None:
        """
        Set the player from a dictionary
        :param data:
        :return:
        """
        self.name = data["name"]
        self.gender = data["gender"]
        self.position = pygame.math.Vector2(data["position"]["x"], data["position"]["y"])
        self.align_hitbox()
        self.direction = data["direction"]
        self.pokemons = [Pokemon.from_dict(pokemon) for pokemon in data["pokemons"]]
        self.inventory = data["inventory"]
        self.pokedex = data["pokedex"]
        self.pokedollars = data["pokedollars"]
        self.ingame_time = datetime.timedelta(seconds=data["ingame_time"])


    def update(self) -> None:
        """
        Update the player
        :return:
        """
        self.update_ingame_time()
        if self.can_move:
            self.check_move()
        self.check_input()
        super().update()

    def check_move(self) -> None:
        """
        Check the move of the player
        :return:
        """
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(self.controller.get_key("left")):
                temp_hitbox.x -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_left()
                else:
                    self.direction = "left"
            elif self.keylistener.key_pressed(self.controller.get_key("right")):
                temp_hitbox.x += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"
            elif self.keylistener.key_pressed(self.controller.get_key("up")):
                temp_hitbox.y -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"
            elif self.keylistener.key_pressed(self.controller.get_key("down")):
                temp_hitbox.y += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"

    def add_switchs(self, switchs: list[Switch]) -> None:
        """
        Add the switchs to the player
        :param switchs:
        :return:
        """
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox) -> None:
        """
        Check the collisions with the switchs
        :param temp_hitbox:
        :return:
        """
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
        return

    def add_collisions(self, collisions) -> None:
        """
        Add the collisions to the player
        :param collisions:
        :return:
        """
        self.collisions = collisions

    def check_collisions(self, temp_hitbox: pygame.Rect) -> bool:
        """
        Check the collisions with the map
        :param temp_hitbox:
        :return:
        """
        for collision in self.collisions:
            if temp_hitbox.colliderect(collision):
                return True
        return False

    def check_input(self) -> None:
        """
        Check the input of the player
        :return:
        """
        if self.animation_walk:
            return
        if self.keylistener.key_pressed(self.controller.get_key("bike")):
            self.switch_bike()
        if self.keylistener.key_pressed(self.controller.get_key("quit")):
            self.menu_option = True
            self.keylistener.remove_key(self.controller.get_key("quit"))
            return

    def switch_bike(self, deactive=False) -> None:
        """
        Switch the bike
        :param deactive:
        :return:
        """
        if self.speed == 1 and not deactive:
            self.speed = 4
            self.all_images = self.get_all_images(self.spritesheet_bike)
        else:
            self.speed = 1
            self.all_images = self.get_all_images(self.spritesheet)
        self.keylistener.remove_key(pygame.K_b)

    def update_ingame_time(self) -> None:
        """
        Update the ingame time
        :return:
        """
        if self.screen.get_delta_time() > 0:
            self.ingame_time += datetime.timedelta(seconds=self.screen.get_delta_time() / 1000)
