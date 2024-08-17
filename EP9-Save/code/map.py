import json
import os
import pathlib

import pygame
import pyscroll
import pytmx

from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from controller import Controller
from player import Player
from screen import Screen
from sql import SQL
from switch import Switch
from tool import Tool


class Map:
    """
    Map class to manage the map
    """
    def __init__(self, screen: Screen, controller: Controller, current_save: str = ""):
        """
        Initialize the map
        :param screen:
        :param controller:
        """
        self.screen: Screen = screen
        self.controller: Controller = controller
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None

        self.player: Player | None = None
        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.sql: SQL = SQL()

        self.current_map: Switch | None = None
        self.map_name: str | None = None
        self.map_name_text: None | str = None

        self.image_change_map: pygame.image = pygame.image.load("../../assets/interfaces/maps/frame_map.png").convert_alpha()
        self.animation_change_map: int = 0
        self.animation_change_map_active: bool = False

        self.current_save: str = ""

    def switch_map(self, switch: Switch) -> None:
        """
        Switch the map
        :param switch:
        :return:
        """
        path = f"../../assets/saves/{self.current_save}/{switch.name}.tmx" if self.current_save else f"../../assets/map/{switch.name}.tmx"
        self.tmx_data = pytmx.load_pygame(path)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=9)
        self.animation_change_map = 0
        self.animation_change_map_active = False

        if switch.name.split("_")[0] == "map":
            self.map_layer.zoom = 3
            self.set_draw_change_map(switch.name)
        else:
            self.map_layer.zoom = 4

        self.switchs = []
        self.collisions = []

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            type = obj.name.split(" ")[0]
            if type == "switch":
                self.switchs.append(Switch(
                    type, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                    int(obj.name.split(" ")[-1])
                ))

        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collisions(self.collisions)
            self.group.add(self.player)
            if switch.name.split("_")[0] != "map":
                self.player.switch_bike(True)

        self.current_map = switch

    def add_player(self, player) -> None:
        """
        Add the player to the map
        :param player:
        :return:
        """
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.collisions)

    def update(self) -> None:
        """
        Update the map
        :return:
        """
        if self.player:
            if self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None
        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

        if self.animation_change_map_active:
            self.draw_change_map()

    def pose_player(self, switch: Switch) -> None:
        """
        Pose the player on the map
        :param switch:
        :return:
        """
        position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)


    def set_draw_change_map(self, map_name: str) -> None:
        """
        Set the draw change map
        :param map_name:
        :return:
        """
        if not self.animation_change_map_active:
            self.map_name = self.sql.get_name_map(map_name)
            self.animation_change_map_active = True
            self.animation_change_map = 0
            self.map_name_text = Tool().create_text(self.map_name, 30, (255, 255, 255))

    def get_surface_change_map(self, alpha: int = 0) -> pygame.Surface:
        """
        Get the surface change map
        :param alpha:
        :return:
        """
        surface_change_map = pygame.Surface((215, 53), pygame.SRCALPHA).convert_alpha()
        surface_change_map.blit(self.image_change_map, (0, 0))
        surface_change_map.set_alpha(alpha)
        return surface_change_map

    def draw_change_map(self) -> None:
        """
        Draw the change map animation
        :return:
        """
        if self.animation_change_map < 255:
            surface = self.get_surface_change_map(self.animation_change_map).convert_alpha()
            self.screen.display.blit(surface, (self.screen.display.get_width() - self.animation_change_map, 600))
            self.animation_change_map += 5
        elif self.animation_change_map < 1024:
            surface = self.get_surface_change_map(255)
            Tool.add_text_to_surface(surface, self.map_name_text,
                                     surface.get_width() // 2 - self.map_name_text.get_width() // 2, 4)
            self.screen.display.blit(surface, (self.screen.display.get_width() - 255, 600))
            self.animation_change_map += 2
        elif self.animation_change_map < 1279:
            surface = self.get_surface_change_map(1279 - self.animation_change_map)
            Tool.add_text_to_surface(surface, self.map_name_text,
                                     surface.get_width() // 2 - self.map_name_text.get_width() // 2, 4)
            self.screen.display.blit(surface, (self.screen.display.get_width() - 255, 600))
            self.animation_change_map += 5
        else:
            self.animation_change_map_active = False
            self.animation_change_map = 0


    def load_map(self, map: str) -> None:
        """
        Load the map from the save
        :param path_save:
        :param map:
        :return:
        """
        self.switch_map(Switch("switch", map, pygame.Rect(0, 0, 0, 0), 0))
