import re
import time

import pandas as pd
import pygame.font

from player import Player
from screen import Screen


class Dialogue:
    def __init__(self, player: Player, screen: Screen):
        self.player = player
        self.screen = screen

        self.number: int | None = None
        self.id: int | None = None

        self.active: bool = False

        self.speakers: list[str] = []
        self.texts: list[str] = []

        self.dialogue_screen: DialogueScreen | None = None
        self.dialogue_data: DialogueData | None = None

    def load_data(self, number: int, id: int):
        self.player.can_move = False
        self.number = number
        self.id = id

        self.dialogue_data = DialogueData(number, id)
        self.active = True

        self.dialogue_screen = DialogueScreen(self.screen, dialogue_data=self.dialogue_data)

    def update(self):
        self.dialogue_screen.update()

    def action(self):
        if self.dialogue_screen.finished:
            self.active = False
            self.player.can_move = True


def format_text(text: str, line_length: int = 100, max_lines: int = 10) -> str:
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
    def __init__(self, number: int, id: int):
        self.speaker_name: str = ""
        self.speaker_image: str = ""
        self.text: str = ""

        self.load_data(number, id)

    def load_data(self, number: int, id: int):
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
        pattern = r':\[name=(.*?);face=(.*?)\]:(.*)'

        match = re.match(pattern, string)

        if match:
            self.speaker_name = match.group(1).strip()
            self.speaker_image = match.group(2).strip().split(',')
            self.text = format_text(match.group(3).strip())

    def __str__(self):
        return (f"Speaker name: {self.speaker_name},\n"
                f"Speaker image: {self.speaker_image},\n"
                f"Text: {self.text}")


class DialogueScreen:
    def __init__(self, screen: Screen, dialogue_data: DialogueData, speed: int = 0.5) -> None:
        self.screen: Screen = screen
        self.dialogue_data: DialogueData = dialogue_data
        self.speed: int = speed

        self.font: pygame.font.Font = pygame.font.Font("../../assets/fonts/OakSans-Regular.ttf", 22)
        self.surface: pygame.Surface = pygame.Surface((1280, 131), pygame.SRCALPHA)
        self.background = pygame.image.load("../../assets/interfaces/dialogues/message_box_0.png").convert_alpha()
        self.background_name = pygame.image.load("../../assets/interfaces/dialogues/name_box_0.png").convert_alpha()

        self.speaker_name = self.font.render(self.dialogue_data.speaker_name, True, (255, 255, 255))

        self.time_wait = time.time()
        self.lines = self.dialogue_data.text.split("\n")

        self.lines_index = 0
        self.lines_offset = [0 for _ in range(len(self.lines))]

        self.y_offset = 0
        self.line_waits = {}

        self.finished: bool = False

    def update(self):
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
        self.screen.display.blit(self.surface, (0, 589))
