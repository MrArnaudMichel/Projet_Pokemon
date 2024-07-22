import json
import os
import pathlib

import pygame
import pyscroll
import pytmx

from controller import Controller
from player import Player
from screen import Screen
from switch import Switch
from sql import SQL
from tool import Tool





class Map:
    def __init__(self, screen: Screen, controller: Controller):
        self.controller = controller
        self.screen: Screen = screen
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None

        self.player: Player | None = None
        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.sql: SQL = SQL()

        self.current_map: Switch = Switch("switch", "map_0", pygame.Rect(0, 0, 0, 0), 0)
        self.map_name: str | None = None
        self.map_name_text = None

        self.image_change_map = pygame.image.load("../../assets/interfaces/maps/frame_map.png").convert_alpha()
        self.animation_change_map = 0
        self.animation_change_map_active = False

        self.switch_map(self.current_map)

    def switch_map(self, switch: Switch) -> None:
        self.tmx_data = pytmx.load_pygame(f"../../assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)
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
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.collisions)

    def update(self) -> None:
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
        position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)

    def save_in_file(self, path: str):
        if not pathlib.Path(f"../../assets/saves/{path}/maps/{self.current_map.name}").exists():
            os.makedirs(f"../../assets/saves/{path}/maps/{self.current_map.name}")
        with open(f"../../assets/saves/{path}/maps/{self.current_map.name}", "w") as file:
            json.dump(self.tmx_data.tiledgidmap, file)
        for i, layer in enumerate(self.tmx_data.visible_layers):
            with open(f"../../assets/saves/{path}/maps/{self.current_map.name}/layer{i}", "w") as file:
                json.dump(layer.data, file)

    def set_draw_change_map(self, map_name: str):
        if not self.animation_change_map_active:
            self.map_name = self.sql.get_name_map(map_name)
            self.animation_change_map_active = True
            self.animation_change_map = 0
            self.map_name_text = Tool().create_text(self.map_name, 30, (255, 255, 255))

    def get_surface_change_map(self, alpha: int = 0):
        surface_change_map = pygame.Surface((215, 53), pygame.SRCALPHA).convert_alpha()
        surface_change_map.blit(self.image_change_map, (0, 0))
        surface_change_map.set_alpha(alpha)
        return surface_change_map

    def draw_change_map(self):
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
