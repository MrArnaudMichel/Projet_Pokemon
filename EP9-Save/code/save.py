import datetime
import json
import os
import pathlib
from time import sleep

from map import Map
from player import Player
from sql import SQL
from keylistener import KeyListener
from dialogue import Dialogue

class Save:
    """
    Save class to manage the save
    """
    def __init__(self, path: str, map: Map, player: Player, keylistener: KeyListener, dialogue: Dialogue):
        """
        Initialize the save
        :param path:
        :param map:
        """
        self.path: str = path
        self.map: Map = map
        self.player: Player = player
        self.keylistener: KeyListener = keylistener
        self.dialogue: Dialogue = dialogue
        self.sql: SQL = SQL()

    def save(self) -> None:
        """
        Save the game
        :return:
        """
        position = self.player.position
        player_info = {
            "name": self.player.name,
            "gender": self.player.gender,
            "position": {
                "x": position[0],
                "y": position[1]
            },
            "direction": self.player.direction,
            "pokemons": [pokemon.to_dict() for pokemon in self.player.pokemons],
            "inventory": self.player.inventory,
            "pokedex": self.player.pokedex,
            "pokedollars": self.player.pokedollars,
            "ingame_time": self.player.ingame_time.seconds
        }
        map_info = {
            "path": self.map.current_map.name,
            "map_name": self.map.map_name
        }
        data = {
            "player": player_info,
            "map": map_info
        }
        if not pathlib.Path(f"../../assets/saves/{self.path}/data.pkmn").exists():
            os.makedirs(f"../../assets/saves/{self.path}")
            pathlib.Path(f"../../assets/saves/{self.path}/data.pkmn").touch()

        with open(f"../../assets/saves/{self.path}/data.pkmn", "w") as file:
            file.write(self.dump(data))

        self.dialogue.load_data(100, 0)

    def load(self) -> None:
        """
        Load the game from the save
        :return:
        """
        if pathlib.Path(f"../../assets/saves/{self.path}/data.pkmn").exists():
            with open(f"../../assets/saves/{self.path}/data.pkmn", "r") as file:
                data = json.load(file)
            self.map.load_map(data["map"]["path"])
            self.player.from_dict(data["player"])
        else:
            self.map.load_map("map_0")
            self.player.set_position(512, 288)
        self.map.add_player(self.player)


    def dump(self, element: dict) -> str:
        """
        Dump the element in json format
        :param element:
        :return:
        """
        return json.dumps(element, indent=4)
