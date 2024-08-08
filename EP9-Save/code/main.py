"""
This is the main file of the game. It initializes the game and runs it.
"""
import pygame

from game import Game

pygame.init()

if __name__ == "__main__":
    game: Game = Game()
    game.run()
