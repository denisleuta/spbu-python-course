from project.game.roulette_game import RouletteGame
from project.bots.conservative_bot import ConservativeBot
from project.bots.aggressive_bot import AggressiveBot
from project.bots.random_bot import RandomBot
from project.bots.only_green_bot import OnlyGreenBot
from project.bots.strategic_bot import StrategicBot


def main():
    bots = [
        ConservativeBot(name="Arthur", budget=100),
        AggressiveBot(name="Denis", budget=100),
        RandomBot(name="Misha", budget=100),
        OnlyGreenBot(name="Mark", budget=100),
        StrategicBot(name="Regina", budget=100),
    ]
    game = RouletteGame(bots)
    game.play()


if __name__ == "__main__":
    main()
