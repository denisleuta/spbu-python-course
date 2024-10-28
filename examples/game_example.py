import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.roulette import ( RouletteGame, ConservativeBot, AggressiveBot, RandomBot)

bots = [
    ConservativeBot(name="ConservativeBot", budget=100),
    AggressiveBot(name="AggressiveBot", budget=100),
    RandomBot(name="RandomBot", budget=100)
]

game = RouletteGame(bots)
game.play()