import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.roulette import (
    RouletteGame,
    ConservativeBot,
    AggressiveBot,
    RandomBot,
    OnlyGreenBot,
)

bots = [
    ConservativeBot(name="Arthur", budget=100),
    AggressiveBot(name="Denis", budget=100),
    RandomBot(name="Misha", budget=100),
    OnlyGreenBot(name="Mark", budget=100),
]

game = RouletteGame(bots)
game.play()
