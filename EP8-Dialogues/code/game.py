import pygame

from controller import Controller
from keylistener import KeyListener
from map import Map
from option import Option
from player import Player
from save import Save
from screen import Screen
from dialogue import Dialogue


class Game:
    """
    Game class to manage the game
    """
    def __init__(self) -> None:
        """
        Initialize the game
        """
        self.running: bool = True
        self.screen: Screen = Screen()
        self.controller = Controller()
        self.map: Map = Map(self.screen, self.controller)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.screen, self.controller, 512, 288, self.keylistener)
        self.map.add_player(self.player)
        self.save: Save = Save("save_0", self.map)
        self.option: Option = Option(self.screen, self.controller, self.map, "fr", self.save, self.keylistener)
        self.dialogue: Dialogue = Dialogue(self.player, self.screen)

    def run(self) -> None:
        """
        Run the game
        :return:
        """
        while self.running:
            self.handle_input()
            if not self.player.menu_option:
                self.map.update()
                if pygame.K_e in self.keylistener.keys and not self.dialogue.active:
                    self.dialogue.load_data(1001, 0)
                    self.keylistener.remove_key(pygame.K_e)
                if self.dialogue.active:
                    self.dialogue.update()
                    if pygame.K_e in self.keylistener.keys:
                        self.dialogue.action()
                        self.keylistener.remove_key(pygame.K_e)
            else:
                self.option.update()
            self.screen.update()

    def handle_input(self) -> None:
        """
        Handle the inputs
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)
