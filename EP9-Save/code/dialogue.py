import re
import time

import pandas as pd
import pygame.font

from player import Player
from screen import Screen


class Dialogue:
    """
    Dialogue class to manage the dialogues
    """
    def __init__(self, player: Player, screen: Screen) -> None:
        """
        Initialize the dialogue
        :param player:
        :param screen:
        """
        self.player: Player = player
        self.screen: Screen = screen

        self.number: int | None = None
        self.id: int | None = None

        self.active: bool = False

        self.speakers: list[str] = []
        self.texts: list[str] = []

        self.dialogue_screen: DialogueScreen | None = None
        self.dialogue_data: DialogueData | None = None

    def load_data(self, number: int, id: int) -> None:
        """
        Load the dialogue data
        :param number:
        :param id:
        :return:
        """
        self.player.can_move = False
        self.number = number
        self.id = id

        self.dialogue_data = DialogueData(number, id)
        self.active = True

        self.dialogue_screen = DialogueScreen(self.screen, dialogue_data=self.dialogue_data, speakers=self.speakers)

    def update(self) -> None:
        """
        Update the dialogue
        :return:
        """
        self.dialogue_screen.update()

    def action(self) -> None:
        """
        Action to do when the dialogue is finished
        :return:
        """
        if self.dialogue_screen.finished:
            self.active = False
            self.player.can_move = True


def format_text(text: str, line_length: int = 100, max_lines: int = 10) -> str:
    """
    Format the text to fit the dialogue box
    :param text:
    :param line_length:
    :param max_lines:
    :return:
    """
    words = text.split()
    formatted_line = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            current_line += (word + " ")
        else:
            formatted_line.append(current_line.strip())
            current_line = ""
            if len(formatted_line) >= max_lines - 1:
                break

    if len(formatted_line) < max_lines:
        formatted_line.append(current_line.strip())
    if len(formatted_line) > max_lines:
        formatted_line = formatted_line[:max_lines]

    return "\n".join(formatted_line)


class DialogueData:
    """
    Dialogue data class to manage the
    """
    def __init__(self, number: int, id: int) -> None:
        self.speaker_name: str = ""
        self.speaker_image: str = ""
        self.text: str = ""

        self.load_data(number, id)

    def load_data(self, number: int, id: int):
        """
        Load the data from the csv file
        :param number:
        :param id:
        :return:
        """
        file_path = f"../../assets/dialogues/{number}.csv"

        df = pd.read_csv(file_path)

        i = id
        column_name = "fr"

        if i in df.index and column_name in df.columns:
            value = df.loc[i, column_name]
        else:
            value = "error"
            print(f"line {i} or column {column_name} not found")

        self.extract_data(value)

    def extract_data(self, string: str):
        """
        Extract the data from the string
        :param string:
        :return:
        """
        pattern = r':\[name=(.*?);face=(.*?)\]:(.*)'

        match = re.match(pattern, string)

        if match:
            self.speaker_name = match.group(1).strip()
            self.speaker_image = match.group(2).strip().split(',')
            self.text = format_text(match.group(3).strip())

    def __str__(self) -> str:
        """
        String representation of the class
        :return:
        """
        return (f"Speaker name: {self.speaker_name},\n"
                f"Speaker image: {self.speaker_image},\n"
                f"Text: {self.text}")


class DialogueScreen:
    """
    Dialogue screen class to manage the dialogue screen
    """
    def __init__(self, screen: Screen, dialogue_data: DialogueData, speed: int = 0.5, speakers=None):
        """
        Initialize the dialogue screen
        :param screen:
        :param dialogue_data:
        :param speed:
        :param speakers:
        """
        if speakers is None:
            speakers = []
        self.screen: Screen = screen
        self.dialogue_data: DialogueData = dialogue_data
        self.speed: int = speed
        self.speakers: list[str] = speakers

        self.font: pygame.font.Font = pygame.font.Font("../../assets/fonts/OakSans-Regular.ttf", 22)
        self.surface: pygame.Surface = pygame.Surface((1280, 131), pygame.SRCALPHA)
        self.background: pygame.Surface = pygame.image.load("../../assets/interfaces/dialogues/message_box_0.png").convert_alpha()
        self.background_name: pygame.Surface = pygame.image.load("../../assets/interfaces/dialogues/name_box_0.png").convert_alpha()

        self.speaker_name: pygame.Surface = self.font.render(self.dialogue_data.speaker_name, True, (255, 255, 255))
        self.speaker_image: pygame.Surface = pygame.image.load(
            f"../../assets/interfaces/characters/battlers/{self.dialogue_data.speaker_image[1]}.png").convert_alpha()
        self.player_image: pygame.Surface = pygame.image.load(
            f"../../assets/interfaces/characters/battlers/heros_swan_big.png").convert_alpha()

        self.time_wait: time = time.time()
        self.lines: list[str] = self.dialogue_data.text.split("\n")

        self.lines_index: int = 0
        self.lines_offset: list[int] = [0 for _ in range(len(self.lines))]

        self.y_offset: int = 0
        self.line_waits: dict[int: int] = {}

        self.speaker_offset: int = 0

        self.finished: bool = False

    def update(self) -> None:
        """
        Update the dialogue screen
        :return:
        """
        wait_time = self.speed * (1 / 60)
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.background, (0, 0))

        for index, line in enumerate(self.lines):
            if index > self.lines_index:
                break
            wait_match = re.search(r'\[WAIT (\d+)]', line)
            if wait_match:
                match = re.finditer(r'\[WAIT (\d+)]', line)
                for m in match:
                    self.line_waits[m.start()] = int(m.group(1)) / 60
                line = re.sub(r'\[WAIT (\d+)]', '', line)
                self.lines[index] = line

            if self.line_waits.__contains__(self.lines_offset[index]):
                wait_time = self.line_waits[self.lines_offset[index]]

            if time.time() - self.time_wait > wait_time and self.lines_offset[index] < len(line):
                self.time_wait = time.time()
                self.lines_offset[index] += 1

                if 2 <= self.lines_index < len(self.lines) - 1 and len(line) - 32 <= self.lines_offset[index]:
                    self.y_offset += 1

                if self.lines_offset[index] == len(line):
                    self.lines_index += 1

            text = line[:self.lines_offset[index]]
            text_surface = self.font.render(text, True, (255, 255, 255)).convert_alpha()
            self.surface.blit(text_surface, (124, (12 + 32 * index) - self.y_offset))

        if self.lines_offset[-1] == len(self.lines[-1]):
            self.finished = True

        if self.dialogue_data.speaker_name != "error":
            if self.dialogue_data.speaker_name == "heros":
                self.screen.display.blit(self.player_image, (-128, 78))
                self.screen.display.blit(self.background_name, (-8, 480))
                self.screen.display.blit(self.speaker_name, (
                    -8 + self.background_name.get_width() // 2 - self.speaker_name.get_width() // 2, 488))
            else:
                if self.dialogue_data.speaker_name not in self.speakers:
                    if self.speaker_offset > 128:
                        self.speakers.append(self.dialogue_data.speaker_name)
                    else:
                        self.speaker_offset += 1

                self.screen.display.blit(self.speaker_image, (1280 - self.speaker_image.get_width() + 128 - self.speaker_offset,
                                                              78))
                self.screen.display.blit(self.background_name,
                                         (1280 - 124 - self.background_name.get_width() // 2, 480))
                self.screen.display.blit(self.speaker_name, (
                    1280 - 124 - self.background_name.get_width() // 2 + self.background_name.get_width() // 2 - self.speaker_name.get_width() // 2,
                    488))
        self.screen.display.blit(self.surface, (0, 589))
