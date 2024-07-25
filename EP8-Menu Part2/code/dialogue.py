import re
import time

import pandas as pd
import pygame

from player import Player
from screen import Screen


class Dialogue:
    def __init__(self, player: Player, screen: Screen) -> None:
        self.dialogue_screen = None
        self.player: Player = player
        self.number: int | None = None
        self.id: int | None = None
        self.screen: Screen = screen
        self.active: bool = False

        self.speakers: list[str] = []
        self.texts: list[str] = []
        self.dialogue_data: DialogueData | None = None

    def load_data(self, number: int, id: int) -> None:
        self.player.can_move = False
        self.number = number
        self.id = id

        self.dialogue_data = DialogueData(number, id)
        self.active = True

        self.dialogue_screen = DialogueScreen(self.screen, self.dialogue_data)

    def update(self):
        self.dialogue_screen.update()

    def action(self) -> None:
        print("Action")
        if self.active:
            print("Active")
            if self.dialogue_screen.finished:
                print("Finished")
                try:
                    print("Try")
                    self.id += 1
                    self.dialogue_data.load_data(self.number, self.id)
                    self.dialogue_screen = DialogueScreen(self.screen, self.dialogue_data)
                    if self.dialogue_data.text == "error":
                        self.active = False
                        self.player.can_move = True
                        print("Dialogue finished")
                    print("Dialogue loaded")
                except:
                    self.active = False
                    self.player.can_move = True
                    print("Dialogue finished")


def format_text(text: str, line_length: int = 100, max_lines: int = 10) -> str:
    words = text.split()
    formatted_lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            current_line += (word + " ")
        else:
            formatted_lines.append(current_line.strip())
            current_line = word + " "
            if len(formatted_lines) >= max_lines - 1:
                break

    # Handle remaining words if any
    if len(formatted_lines) < max_lines:
        formatted_lines.append(current_line.strip())

    if len(formatted_lines) > max_lines:
        formatted_lines = formatted_lines[:max_lines]
    else:
        formatted_lines += [""] * (max_lines - len(formatted_lines))

    return "\n".join(formatted_lines)


class DialogueData:
    def __init__(self, number: int, id: int) -> None:
        self.speaker_name: str = ""
        self.speaker_image: str = ""
        self.text: str = ""

        self.load_data(number, id)

    def load_data(self, number: int, id: int) -> None:
        file_path = f"../../assets/dialogues/{number}.csv"

        df = pd.read_csv(file_path)

        i = id
        column_name = 'fr'

        if i in df.index and column_name in df.columns:
            value = df.loc[i, column_name]
        else:
            value = "error"
            print(f"line {i} or column '{column_name}' not found")

        self.extract_data(value)

    def extract_data(self, string: str):
        pattern = r':\[name=(.*?);face=(.*?)\]:(.*)'
        match = re.match(pattern, string)

        if match:
            self.speaker_name = match.group(1).strip()
            self.speaker_image = match.group(2).strip().split(",")
            self.text = format_text(match.group(3).strip())
        else:
            print("The string format is incorrect.")
            self.speaker_name = "error"
            self.speaker_image = "error"
            self.text = string

    def __str__(self):
        return f"Speaker Name: {self.speaker_name}\nSpeaker Image: {self.speaker_image}\nText: {self.text}"


class DialogueScreen:
    def __init__(self, screen: Screen, dialogue_data: DialogueData, speed: int = 0.1) -> None:
        self.speed: int = speed
        self.screen: Screen = screen
        self.dialogue_data: DialogueData = dialogue_data

        self.font: pygame.font.Font = pygame.font.Font("../../assets/fonts/OakSans-Regular.ttf", 22)
        self.surface = pygame.Surface((1280, 131), pygame.SRCALPHA)
        self.background = pygame.image.load("../../assets/interfaces/dialogues/message_box_0.png").convert_alpha()
        self.background_name = pygame.image.load("../../assets/interfaces/dialogues/name_box_0.png").convert_alpha()

        self.speaker_name = self.font.render(self.dialogue_data.speaker_name, True, (255, 255, 255))
        self.speaker_image = pygame.image.load(
            f"../../assets/interfaces/characters/battlers/{self.dialogue_data.speaker_image[1]}.png").convert_alpha()
        self.player_image = pygame.image.load(
            f"../../assets/interfaces/characters/battlers/heros_swan_big.png").convert_alpha()

        self.time_wait = time.time()
        self.lines = self.dialogue_data.text.split('\n')

        self.lines = [line for line in self.lines if line.strip() != ""]

        self.lines_index = 0
        self.lines_offset = [0 for _ in range(len(self.lines))]
        self.y_offset = 0

        self.finished = False

    def update(self) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.background, (0, 0))

        for index, line in enumerate(self.lines):
            if index > self.lines_index:
                break
            wait_match = re.search(r'\[WAIT (\d+)]', line)
            if wait_match:
                wait_time = int(wait_match.group(1)) / 60
                line = re.sub(r'\[WAIT \d+]', '', line)
            else:
                wait_time = self.speed * (1 / 60)

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
                self.screen.display.blit(self.speaker_image, (1280 - self.speaker_image.get_width() + 128,
                                                              78))
                self.screen.display.blit(self.background_name,
                                         (1280 - 124 - self.background_name.get_width() // 2, 480))
                self.screen.display.blit(self.speaker_name, (
                    1280 - 124 - self.background_name.get_width() // 2 + self.background_name.get_width() // 2 - self.speaker_name.get_width() // 2,
                    488))
        self.screen.display.blit(self.surface, (0, 589))