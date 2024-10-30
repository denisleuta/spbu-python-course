import pytest
import sys
import os
from typing import Type

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.roulette import RouletteGame
from project.game.bet import Bet
from project.bots.bot import StrategyMeta, Bot
from project.game.game_rule_meta import GameRuleMeta


@pytest.fixture
def setup_game() -> RouletteGame:
    bot_names = ["Arthur", "Denis", "Misha"]
    bot_budgets = [100, 100, 100]
    bot_strategies = ["AggressiveBot", "OnlyGreenBot", "StrategicBot"]

    bots = [
        StrategyMeta.create_strategy(strategy, name=name, budget=budget)
        for strategy, name, budget in zip(bot_strategies, bot_names, bot_budgets)
    ]

    game = RouletteGame(bots)
    return game


def test_initial_state(setup_game: RouletteGame) -> None:
    game = setup_game
    assert game.round == 1
    for bot in game.bots:
        assert bot.budget == 100


def test_spin_wheel(setup_game: RouletteGame) -> None:
    game = setup_game
    number, color = game.spin_wheel()
    assert 0 <= number < game.NUMBER_OF_FIELDS
    assert color in game.COLORS


def test_budget_update(setup_game: RouletteGame) -> None:
    game = setup_game
    bot = game.bots[0]
    initial_budget = bot.budget
    bot.update_budget(50)
    assert bot.budget == initial_budget + 50


def test_bet_evaluation_color(setup_game: RouletteGame) -> None:
    game = setup_game
    winning_number = 1
    winning_color = "Red"
    bet = Bet(amount=10, bet_type="color", choice="Red")
    result = game.evaluate_bets(bet, winning_number, winning_color)
    assert result == 20


def test_bet_evaluation_number(setup_game: RouletteGame) -> None:
    game = setup_game
    winning_number = 17
    winning_color = "Black"
    bet = Bet(amount=10, bet_type="number", choice=17)
    result = game.evaluate_bets(bet, winning_number, winning_color)
    assert result == 360


def test_bet_evaluation_green(setup_game: RouletteGame) -> None:
    game = setup_game
    winning_number = 0
    winning_color = "Green"
    bet = Bet(amount=10, bet_type="color", choice="Green")
    result = game.evaluate_bets(bet, winning_number, winning_color)
    assert result == 350


def test_play_round(setup_game: RouletteGame) -> None:
    game = setup_game
    initial_budgets = [bot.budget for bot in game.bots]
    game.play_round()
    assert game.round == 2
    assert any(bot.budget != initial_budgets[i] for i, bot in enumerate(game.bots))


def test_game_progression(setup_game: RouletteGame) -> None:
    game = setup_game
    game.play()
    assert game.round > 1
    assert game.round <= game.max_steps + 1 or all(bot.budget <= 0 for bot in game.bots)


def test_winning_condition(setup_game: RouletteGame) -> None:
    game = setup_game
    bot = game.bots[0]
    bot.update_budget(game.WINNING_BUDGET - bot.budget)
    winner = game.check_for_winner()
    assert winner is not None
    assert winner.budget >= game.WINNING_BUDGET


def test_game_rule_meta_constants():
    assert RouletteGame.NUMBER_OF_FIELDS == 50, "NUMBER_OF_FIELDS must be equal 50"
    assert RouletteGame.WINNING_BUDGET == 1000, "WINNING_BUDGET must be equal 1000"


def test_custom_class_with_game_rule_meta():
    class CustomGame(metaclass=GameRuleMeta):
        pass

    assert (
        CustomGame.NUMBER_OF_FIELDS == 50
    ), "NUMBER_OF_FIELDS must be equal 50 in CustomGame"
    assert (
        CustomGame.WINNING_BUDGET == 1000
    ), "WINNING_BUDGET must be equal 1000 in CustomGame"


class DummyStrategy(Bot):
    def place_bet(self):
        return None


class AnotherStrategy(Bot):
    def place_bet(self):
        return None


def test_strategy_registration():
    strategies = StrategyMeta.get_strategies()
    assert "DummyStrategy" in strategies, "DummyStrategy should be registered"
    assert "AnotherStrategy" in strategies, "AnotherStrategy should be registered"


def test_create_strategy_instance():
    dummy_instance = StrategyMeta.create_strategy(
        "DummyStrategy", name="TestBot", budget=100
    )
    assert isinstance(
        dummy_instance, DummyStrategy
    ), "The instance should be of type DummyStrategy"
    assert dummy_instance.name == "TestBot", "The instance name should match 'TestBot'"
    assert dummy_instance.budget == 100, "The instance budget should match 100"
