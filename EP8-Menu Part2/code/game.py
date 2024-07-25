import pygame

from controller import Controller
from dialogue import Dialogue
from keylistener import KeyListener
from map import Map
from option import Option
from player import Player
from save import Save
from screen import Screen


class Game:
    def __init__(self) -> None:
        self.running: bool = True
        self.screen: Screen = Screen()
        self.controller = Controller()
        self.map: Map = Map(self.screen, self.controller)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.screen, self.controller, 512, 288, self.keylistener)
        self.map.add_player(self.player)
        self.save = Save("save_0", self.map)
        self.option = Option(self.screen, self.controller, self.map, "fr", self.save, self.keylistener)
        self.dialogue = Dialogue(self.player, self.screen)

    def run(self) -> None:
        while self.running:
            self.handle_input()
            if not self.player.menu_option:
                self.map.update()
                if self.dialogue.active:
                    self.dialogue.update()
                    if pygame.K_e in self.keylistener.keys:
                        self.dialogue.action()
                else:
                    if pygame.K_e in self.keylistener.keys:
                        self.dialogue.load_data(1096, 0)
                self.keylistener.remove_key(pygame.K_e)
            else:
                self.option.update()
            self.screen.update()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)
