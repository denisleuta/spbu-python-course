import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.game.roulette import RouletteGame
from project.bots.bot import StrategyMeta

available_strategies = StrategyMeta.get_strategies()
print("Available strategies:", available_strategies)

bots = [
    StrategyMeta.create_strategy("AggressiveBot", name="Denis", budget=100),
    StrategyMeta.create_strategy("OnlyGreenBot", name="Mark", budget=100),
    StrategyMeta.create_strategy("StrategicBot", name="Regina", budget=100),
]

game = RouletteGame(bots)
game.play()
