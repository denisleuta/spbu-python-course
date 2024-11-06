from project.game.roulette_game import RouletteGame
from project.bots.aggressive_bot import AggressiveBot
from project.bots.only_green_bot import OnlyGreenBot
from project.bots.strategic_bot import StrategicBot


def main():
    bots = [
        AggressiveBot(name="Denis", budget=100),
        OnlyGreenBot(name="Mark", budget=100),
        StrategicBot(name="Regina", budget=100),
    ]
    game = RouletteGame(bots)
    game.play()

