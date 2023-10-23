import pygame

from game import Game

pygame.init()

if __name__ == "__main__":
    game: Game = Game()
    game.run()
